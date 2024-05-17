import sys

import src.my_parser as parser
import src.backend as backend


def main():
    args = parser.parse_args()
    res = backend.call(args)
    print(f"[LTL] Hidden Relation:{res}")  # hidden relation with confidence score
    sys.stdout.flush()
    return res


if __name__ == "__main__":
    main()
