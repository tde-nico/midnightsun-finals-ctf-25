import time
from pwn import *
from pulp import LpProblem, LpVariable, LpInteger, lpSum, value, PULP_CBC_CMD

# context.log_level = 'debug'

HOST, PORT = ("speedmisc.play.hfsc.tf", 1337)
ROWS = 9

def read_banner(r):
    r.recvuntil(b"values:")
    nums_line = r.recvline()
    nums = [int(x) for x in nums_line.split()[1:-1]]
    # print(nums)
    if len(nums) != ROWS:
        raise ValueError(f"expected {ROWS} numbers, got {len(nums)} – "
                         f"line was {nums_line!r}")
    r.recvuntil(b"target:")
    target = int(r.recvline().split()[1])
    return nums, target

def learn_moves(r):
    start_vec, _ = read_banner(r)
    deltas = []
    for d in range(1, 10):
        r.sendline(str(d).encode())
        after_vec, _ = read_banner(r)
        deltas.append([a - s for a, s in zip(after_vec, start_vec)])
        start_vec = after_vec
        # r.sendline(b"0")
        # read_banner(r)
    # print(deltas)
    return [list(col) for col in zip(*deltas)]

def ilp_solution(A_rows, diff):
    prob = LpProblem("solve")
    k = [LpVariable(f"k{i}", lowBound=0, cat=LpInteger) for i in range(9)]
    for row, rhs in zip(A_rows, diff):
        prob += lpSum(row[i] * k[i] for i in range(9)) == rhs
    prob += lpSum(k)
    prob.solve(PULP_CBC_CMD(msg=0))
    return [int(value(var)) for var in k]


def press_sequence(r, presses):
    cmd = b"".join(str(d).encode() * presses[d-1] for d in range(1, 10))
    if not cmd:
        return
    r.sendline(cmd)
    for _ in range(len(cmd)):
        read_banner(r)


def main():
    r = remote(HOST, PORT)
    for i in range(100):
        try:
            A_rows = learn_moves(r)
            r.sendline(b"0")
            vec, tgt = read_banner(r)
            diff = [tgt - v for v in vec]
            # if i > 98:
            #     context.log_level = 'debug'
            press_sequence(r, ilp_solution(A_rows, diff))
            r.sendline(b"0")
        except ValueError:
            print("SUCCESS!!!!", i)
            continue
    print(r.recvall())
    # r.interactive()


if __name__ == "__main__":
    main()


# midnight{y34H_w3ll_wh4t3v3r}
