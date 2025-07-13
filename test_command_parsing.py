#
from engine.command_parsing import parse_command
#
import os

#
tests_path: str = "tests_command_parsing"

#
test_files: list[tuple[str, str]] = [
    (f"{tests_path}/test1_in.txt", f"{tests_path}/test1_out.txt"),
#    (f"{tests_path}/test2_in.txt", f"{tests_path}/test2_out.txt")
]

#
if __name__ == "__main__":
    #
    generic_kws: dict[str, str] = {
        "to": "KW_TO",
        "in": "KW_IN",
        "into": "KW_IN",
        "inside": "KW_IN",
        "on": "KW_ON",
        "with": "KW_WITH"
    }
    #
    test_file_in: str
    test_file_out: str
    for test_file_in, test_file_out in test_files:
        #
        if not os.path.exists(test_file_in):
            print(f"\033[31mError: file \"{test_file_in}\" not found, test passed.\033[m")
            continue
        #
        if not os.path.exists(test_file_out):
            print(f"\033[31mError: file \"{test_file_out}\" not found, test passed.\033[m")
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
        tests_in = [test for test in tests_in if test]
        tests_out = [test for test in tests_out if test]
        #
        if len(tests_in) != len(tests_out):
            print(f"\033[31mError: not the same number of tests in the files \"{test_file_in}\" and \"{test_file_out}\" !\033[m")
            continue
        #
        if len(tests_in) == 0:
            print(f"\033[33mWarning: empty tests files \"{test_file_in}\" and \"{test_file_out}\" !\033[m")
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
            res: str = f"{parse_command(command_input=test_input, generic_kws=generic_kws)}".strip()
            #
            if res != test_output:
                print(f"\033[31mtest {i} FAILED\033[m\n  - Input: \"{test_input}\"\n  - Awaited output : \"{test_output}\"\n  - Received output : \"{res}\"\n")
                continue
            #
            print(f"\033[32mtest {i} PASSED\033[m")
            nb_passed += 1

        #
        print(f"\nTESTS SUCCESS RATE : {nb_passed} / {len(tests_in)} -> {round(100 * nb_passed / len(tests_in), 3)} %")



