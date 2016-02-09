import tensorflow as tf
import random

from .blocks import (
    parse_block,
    parse_optimizer,
    SequenceWrapper,
)
class EncDec(object):
    def __init__(self, settings, session):
        self.s = session

        self.action_type = settings["action"]["type"]
        if self.action_type == "discrete":
            self.num_actions = settings["action"]["num_actions"]
        else:
            assert False, "Unknown action type:" % (self.action_type,)

        self.create_variables(settings)
        self.s.run(tf.initialize_variables(self.variables()))

    def create_variables(self, settings):
        self.network_names = [
            'state_encoder',
            'action_decoder',
            'value_decoder',
        ]

        self.networks = {
            name:parse_block(settings['networks'][name])
            for name in self.network_names
        }

        self.optimizers   = {
            name:parse_optimizer(settings['optimizers'][name])
            for name in self.network_names
        }


        self.action_network = SequenceWrapper(
            [self.networks["state_encoder"], self.networks["action_decoder"]],
            scope="action_network")

        self.value_network = SequenceWrapper(
            [self.networks["state_encoder"], self.networks["value_decoder"]],
            scope="value_network")

        self.state        = self.networks["state_encoder"].input_placeholder()
        self.action_probs = self.action_network(self.state)
        self.action_id    = tf.argmax(self.action_probs, dimension=1)

        self.value        =  self.value_network(self.state)




    def action(self, state, exploration=0.0):
        if random.random() < exploration:
            return random.randint(0, self.num_actions - 1)
        else:
            return self.s.run(self.action_id, {
                self.state: state,
            })

    def value(self, state):
        return self.s.run(self.value, {
            self.state: state,
        })

    def update_grads(self, R, s, a):
        pass

    def apply_grads(self, GRADS):
        pass

    def variables(self):
        result = []
        for n in self.network_names:
            result.extend(self.networks[n].variables())
        return result

    def get_params(self):
        pass

    def set_params(self, PARAMS):
        pass

    def save(self, directory):
        pass

    def load(self, directory):
        pass