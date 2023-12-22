from streamlitinternalapp.cli import parser
from streamlitinternalapp.module import add

args = parser.parse_args()

print(add(*args.n))
