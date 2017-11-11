import hypothesis.strategies as st
from hypothesis import given, assume, event, settings


def run_length_encode(seq):
    """Encode a sequence as a new run-length encoded sequence."""
    if not seq:
        return []
    # By starting off the count at zero we simplify the iteration logic
    # slightly.
    result = [[seq[0], 0]]
    for s in seq:
        if (
            # If you uncomment this line this branch will be skipped and we'll
            # always append a new run of length 1. Note which tests fail.
            # False and
            s == result[-1][0]
            # Try uncommenting this line and see what problems occur:
            # and result[-1][1] < 2
        ):
            result[-1][1] += 1
        else:
            result.append([s, 1])
    return result


def run_length_decode(seq):
    """Take a previously encoded sequence and reconstruct the original from
    it."""
    result = []
    for s, i in seq:
        for _ in range(i):
            result.append(s)
    return result


# We use lists of a type that should have a relatively high duplication rate,
# otherwise we'd almost never get any runs.


@given(st.lists(st.integers(0, 10)))
def test_decodes_to_starting_sequence(ls):
    """If we encode a sequence and then decode the result, we should get the
    original sequence back.
    Otherwise we've done something very wrong.
    """
    assert run_length_decode(run_length_encode(ls)) == ls


@given(st.lists(st.integers(0, 10), min_size=5))
def test_duplicating_an_element_does_not_increase_length1(ls):
    # Copy the input list
    ls2 = list(ls)
    # Duplicate the element in position 3.
    ls2.insert(3, ls2[3])
    assert len(run_length_encode(ls2)) == len(run_length_encode(ls))


@given(st.lists(st.integers(0, 10)), st.integers(0, 10))
@settings(max_examples=400)
def test_duplicating_an_element_does_not_increase_length(ls, i):
    """The previous test could be passed by simply returning the input sequence
    so we need something that tests the compression property of our encoding.
    In this test we deliberately introduce or extend a run and assert
    that this does not increase the length of our encoding, because they
    should be part of the same run in the final result.
    """
    # We use assume to get a valid index into the list. We could also have used
    # e.g. flatmap, but this is relatively straightforward and will tend to
    # perform better.
    event('Index I was out of bound {}'.format(i > len(ls)))
    assume(i < len(ls))

    ls2 = list(ls)
    # duplicating the value at i right next to it guarantees they are part of
    # the same run in the resulting compression.
    ls2.insert(i, ls2[i])
    assert len(run_length_encode(ls2)) == len(run_length_encode(ls))
