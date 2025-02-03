#
from command_parsing import parse_command
#
import os

#
test_files: list[tuple[str, str]] = [
    ("tests/test1_in.txt", "tests/test1_out.txt")
]

#
if __name__ == "__main__":
    #
    test_file_in: str
    test_file_out: str
    for test_file_in, test_file_out in test_files:
        #
        if not os.path.exists(test_file_in):
            print(f"Error: file \"{test_file_in}\" not found, test passed.")
            continue
        #
        if not os.path.exists(test_file_out):
            print(f"Error: file \"{test_file_out}\" not found, test passed.")
            continue
        #
        tests_in: list[str]
        test_out: list[str]
        #
        with open(test_file_in, "r", encoding="utf-8") as f:
            #
            tests_in = f.read().strip().split("\n")
        #
        with open(test_file_out, "r", encoding="utf-8") as f:
            #
            tests_out = f.read().strip().split("\n")
        #
        if len(tests_in) != len(tests_out):
            print(f"Error: not the same number of tests in the files \"{test_file_in}\" and \"{test_file_out}\" !")
            continue
        #
        if len(tests_in) == 0:
            print(f"Warning: empty tests files \"{test_file_in}\" and \"{test_file_out}\" !")
            continue
        #
        print(f"\nTESTS {test_file_in} | {test_file_out}")
        #
        nb_passed: int = 0
        #
        i: int
        for i in range(len(tests_in)):
            #
            test_input: str = tests_in[i].strip()
            test_output: str = tests_out[i].strip()
            #
            res: str = f"{parse_command(test_input)}".strip()
            #
            if res != test_output:
                print(f"test {i} FAILED\n  - Input: \"{test_input}\"\n  - Awaited output : \"{test_output}\"\n  - Received output : \"{res}\"\n")
                continue
            #
            print(f"test {i} PASSED")
            nb_passed += 1

        #
        print(f"\nTESTS SUCCESS RATE : {nb_passed} / {len(tests_in)} -> {round(100 * nb_passed / len(tests_in), 3)} %")



