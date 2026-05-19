import unittest

import numpy as np

from src.power import CPAAttack, HW, SBOX, aes_internal


def _synthetic_traces(model, key, seed):
    """Build one synthetic power trace per plaintext byte.

    The middle sample carries the signal HW(model(input, key)); the two
    surrounding samples carry input-dependent noise so that no trace column
    is constant (which would divide by a zero standard deviation).
    """
    rng = np.random.default_rng(seed)
    traces = []
    for input_byte in range(256):
        signal = float(HW[model(input_byte, key)])
        noise = rng.standard_normal(2)
        traces.append((input_byte, np.array([noise[0], signal, noise[1]])))
    return traces


class CPALeakageModelTest(unittest.TestCase):

    def test_cpa_uses_supplied_leakage_model(self):
        key = 0x6d
        add_round_key = lambda input_byte, key_guess: input_byte ^ key_guess
        traces = _synthetic_traces(add_round_key, key, seed=1)

        scores = CPAAttack(traces, add_round_key).attack()

        self.assertEqual(int(np.argmax(scores)), key)

    def test_cpa_default_leakage_model_recovers_key(self):
        key = 0x2b
        traces = _synthetic_traces(aes_internal, key, seed=0)

        scores = CPAAttack(traces).attack()

        self.assertEqual(int(np.argmax(scores)), key)


if __name__ == "__main__":
    unittest.main()
