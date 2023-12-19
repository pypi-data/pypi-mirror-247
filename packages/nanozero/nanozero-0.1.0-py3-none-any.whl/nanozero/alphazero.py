# Basically based on AlphaZero pseudo-code

from __future__ import annotations
from functools import partial
import jax
import jax.lax as lax
import jax.numpy as jnp
from typing import NamedTuple, Callable, Tuple, Optional, Literal
import pgx
from collections import namedtuple
import chex
from flax.struct import dataclass, PyTreeNode


InferenceFn = Callable[
    [jax.Array, pgx.State],       # (key, state)
    Tuple[jax.Array, jax.Array]   # (logits, value)
]

NO_PARENT = jnp.int32(-1)
ROOT_IX = jnp.int32(0)


@dataclass
class Tree:
    # num_nodes = num_simulations + 2  (root and sentinel)

    # node attributes
    parent: jax.Array  # (num_nodes,)
    terminated: jax.Array  # (num_nodes,)
    action_from_parent: jax.Array  # (num_nodes,)

    # edge attributes
    _reward: jax.Array  # (num_nodes,)
    _visit_count: jax.Array  # (num_nodes,)
    _value_sum: jax.Array  # (num_nodes,)
    priors: jax.Array  # (num_nodes, num_actions)
    children: jax.Array  # (num_nodes, num_actions)

    # others
    min_empty_index: jax.Array

    @property
    def num_nodes(self) -> int:
        return self.parent.shape[-1]

    @property
    def num_actions(self) -> int:
        return self.children.shape[-1]

    def qvalue(self, parent_ix: jax.Array, action: jax.Array) -> jax.Array:
        n = self.visit_count(parent_ix, action)
        w = self.value_sum(parent_ix, action)
        eps = 1e-9
        q = w / (n + eps)
        return q

    def reward(self, parent_ix: jax.Array, action: jax.Array) -> jax.Array:
        child_ix = self.children[parent_ix, action]
        return jax.lax.select(child_ix >= 0, self._reward[child_ix], 0.0)

    def node_visit_count(self, node_ix: jax.Array) -> jax.Array:
        return jax.vmap(partial(self.visit_count, parent_ix=node_ix))(
            action=jnp.arange(self.num_actions)
        ).sum()

    def visit_count(self, parent_ix: jax.Array, action: jax.Array) -> jax.Array:
        child_ix = self.children[parent_ix, action]
        return jax.lax.select(child_ix >= 0, self._visit_count[child_ix], 0.0)

    def value_sum(self, parent_ix: jax.Array, action: jax.Array) -> jax.Array:
        child_ix = self.children[parent_ix, action]
        return jax.lax.select(child_ix >= 0, self._value_sum[child_ix], 0.0)

    @staticmethod
    def add_child(
        tree: Tree,
        node_ix: jax.Array,
        action: jax.Array,
        terminated: jax.Array,
        reward: jax.Array,
        leaf_priors: jax.Array,
    ) -> Tuple[Tree, jax.Array]:  # tree and new node index
        child_ix = tree.min_empty_index
        return (
            tree.replace(
                parent=tree.parent.at[child_ix].set(node_ix),
                children=tree.children.at[node_ix, action].set(child_ix),
                action_from_parent=tree.action_from_parent.at[child_ix].set(action),
                terminated=tree.terminated.at[child_ix].set(terminated),
                priors=tree.priors.at[child_ix].set(leaf_priors),
                _reward=tree._reward.at[child_ix].set(reward),
                min_empty_index=child_ix + 1,
            ),
            child_ix,
        )

    @classmethod
    def create_tree(cls, num_simulations, num_actions, root_priors: jax.Array):
        num_nodes = num_simulations + 2
        return cls(  # type: ignore
            parent=jnp.full(num_nodes, NO_PARENT, dtype=jnp.int32),
            terminated=jnp.zeros(num_nodes, dtype=jnp.bool_),
            action_from_parent=jnp.full(num_nodes, -1, dtype=jnp.int32),
            _reward=jnp.zeros(num_nodes),
            _visit_count=jnp.zeros(num_nodes),
            _value_sum=jnp.zeros(num_nodes),
            priors=jnp.zeros((num_nodes, num_actions)).at[ROOT_IX].set(root_priors),
            children=-jnp.ones((num_nodes, num_actions), dtype=jnp.int32),
            min_empty_index=jnp.int32(1)
        )


def run_mcts(
    key: jax.Array,
    state: pgx.State,
    env: pgx.Env,
    inference_fn: InferenceFn,
    num_simulations: int,
) -> Tuple[jax.Array, Tree]:
    # prepare root node
    key, subkey = jax.random.split(key)
    priors, _ = evaluate(subkey, state, inference_fn)
    # TODO: add noise
    tree = Tree.create_tree(num_simulations, env.num_actions, priors)

    # main search loop
    def loop_fn(i, x):
        k, t = x
        k, subkey = jax.random.split(k)
        t = update(subkey, t, root_state=state, env=env, inference_fn=inference_fn)
        return k, t

    _, tree = lax.fori_loop(0, num_simulations, loop_fn, (key, tree))

    action = select_action(tree)
    return action, tree


def select_action(tree: Tree) -> jax.Array:
    """Select the action in the real environment based on the search results."""
    visit_counts = jax.vmap(partial(tree.visit_count, parent_ix=ROOT_IX))(
        action=jnp.arange(tree.num_actions)
    )
    return jnp.argmax(visit_counts)


def update(
    key: Optional[jax.Array],
    tree: Tree,
    *,
    root_state: pgx.State,
    env: pgx.Env,
    inference_fn: InferenceFn
):
    """Run one iteration of MCTS."""
    evaluate_key, select_key = jax.random.split(key)

    # select the node to expand
    non_expanded_ix, non_expanded_state, action = select_while(select_key, tree, root_state, env)

    # evaluate the state corresponding to the leaf node
    leaf_state = env.step(non_expanded_state, action)
    leaf_priors, leaf_value = evaluate(evaluate_key, leaf_state, inference_fn)

    # attach the leaf node to the node to expand
    reward = leaf_state.rewards[non_expanded_state.current_player]
    tree, leaf_node_ix = Tree.add_child(
        tree, non_expanded_ix, action, leaf_state.terminated, reward, leaf_priors
    )

    # backpropagate
    tree = backpropagate(tree, leaf_node_ix, leaf_value)

    return tree


def select_while(key: jax.Array, tree: Tree, root_state: pgx.State, env: pgx.Env):
    class LoopState(NamedTuple):
        key: jax.Array
        state: pgx.State
        action: jax.Array
        node_ix: jax.Array = ROOT_IX

    def cond_fn(x: LoopState):
        return tree.children[x.node_ix, x.action] >= 0

    def while_fn(x: LoopState):
        state = env.step(x.state, x.action)
        node_ix = tree.children[x.node_ix, x.action]
        new_key, subkey = jax.random.split(x.key)
        action = select_child(subkey, tree, node_ix, state.legal_action_mask)
        return LoopState(
            key=new_key,
            state=state,
            action=action,
            node_ix=node_ix,
        )

    key, subkey = jax.random.split(key)
    action = select_child(subkey, tree, ROOT_IX, root_state.legal_action_mask)
    out = lax.while_loop(cond_fn, while_fn, LoopState(key=key, state=root_state, action=action))
    return out.node_ix, out.state, out.action


def select_child(
    key: jax.Array, tree: Tree, node_ix: jax.Array, legal_action_mask: jax.Array
) -> jax.Array:
    vucb_score_fn = jax.vmap(partial(ucb_score, tree=tree, parent_ix=node_ix))
    actions = jnp.arange(tree.num_actions)
    scores = vucb_score_fn(action=actions)
    node_noise_score = 1e-7 * jax.random.uniform(key, (tree.num_actions,))
    scores += node_noise_score
    # mask illegal actions. In unvisited nodes, scores are all zeros in AlphaZero.
    scores = jnp.where(legal_action_mask, scores, jnp.finfo(scores.dtype).min)
    action = jnp.argmax(scores)  # type: ignore
    return action


def ucb_score(
    tree: Tree,
    parent_ix: jax.Array,
    action: jax.Array,
    pb_c_base: float = 19652.0,
    pb_c_init: float = 1.25,
):
    parent_visit_count = jax.vmap(partial(tree.visit_count, parent_ix=parent_ix))(
        action=jnp.arange(tree.num_actions)
    ).sum()
    child_visit_count = tree.visit_count(parent_ix, action)
    pb_c = jnp.log((parent_visit_count + pb_c_base + 1) / pb_c_base) + pb_c_init
    pb_c *= jnp.sqrt(parent_visit_count) / (child_visit_count + 1)

    prior_score = pb_c * tree.priors[parent_ix, action]
    value_score = tree.qvalue(parent_ix, action)
    return prior_score + value_score


def evaluate(
    key: jax.Array, state: pgx.State, inference_fn: InferenceFn
) -> Tuple[jax.Array, jax.Array]:
    logits, value = inference_fn(key, state)
    priors = jax.nn.softmax(logits)  # assume already masked
    value = jax.lax.select(state.terminated, 0.0, value)
    return priors, value


def backpropagate(tree: Tree, leaf_node_ix: jax.Array, leaf_value: jax.Array):
    def cond_fn(x):
        _, i, _ = x
        return i != NO_PARENT

    def while_fn(x):
        t, child_ix, v = x
        parent_ix = t.parent[child_ix]
        a = t.action_from_parent[child_ix]
        v = t.reward(parent_ix, a) + (-1.0) * v
        t = t.replace(
            _value_sum=t._value_sum.at[child_ix].add(v),
            _visit_count=t._visit_count.at[child_ix].add(1),
        )
        return t, parent_ix, v

    tree, _, _ = lax.while_loop(cond_fn, while_fn, (tree, leaf_node_ix, leaf_value))
    return tree

