import jax
import jax.numpy as jnp
import equinox


class Seed:
    def __init__(self, seed = 0):
        self._seed = int(seed)
        self.key = jax.random.PRNGKey(seed)
    def __call__(self, num=2):
        self.key, *keys = jax.random.split(self.key, num)
        return jnp.array(keys).squeeze()


def params_to_array(params):
    arrays, unflatten = jax.tree_util.tree_flatten(params)
    flat_arrays = list(map(jnp.ravel, arrays))
    array = jnp.concatenate(flat_arrays)
    return array


## TODO: convert maps to jax transformations
def get_array_to_params(params):
    arrays, unflatten = jax.tree_util.tree_flatten(params)
    shapes = list(map(jnp.shape, arrays))
    lens = list(map(lambda shape: jnp.prod(jnp.array(shape)), shapes))
    idxs = list(jnp.cumsum(jnp.array(lens[:-1])))
    def array_to_params(array):
        flat_arrays = jnp.split(array, idxs)
        arrays = list(map(lambda z: jnp.reshape(*z), zip(flat_arrays, shapes)))
        params = jax.tree_util.tree_unflatten(unflatten, arrays)
        return params
    return array_to_params


def count_params(params):
    return params_to_array(params).size


def save(file, model, filter_spec = equinox.is_inexact_array):
    params = equinox.filter(model, filter_spec)
    array = params_to_array(params)
    return jnp.save(file, array)


def load(file, model, filter_spec = equinox.is_inexact_array):
    params, static = equinox.partition(model, filter_spec)
    array_to_params = get_array_to_params(params)
    array = jnp.load(file)
    params = array_to_params(array)
    model = equinox.combine(params, static)
    return model
