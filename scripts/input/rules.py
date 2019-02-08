import re

# rules = [
#     ('total_words', re.compile(r"\b\w+\b")),
#     ('variable_cost_ct', re.compile(r"\bvariable\b \bcosts?\b")),
#     ('variable_exp_ct', re.compile(r"\bvariable\b \bexpenses?\b")),
#     ('fixed_exp_ct', re.compile(r"\bfixed\b \bexpenses?\b")),
#     ('fixed_cost_ct', re.compile(r"\bfixed\b \bcosts?\b")),
#     ('large_fixed_ct', re.compile(r"\blarge\b \bfixed\b")),
#     ('sign_fixed_ct', re.compile(r"\bsignificant\b \bfixed\b")),
#     ('rel_fixed_ct', re.compile(r"\brelatively\b \bfixed\b")),
#     ('mostly_fixed_ct', re.compile(r"\bmostly\b \bfixed\b")),
#     ('just_in_time_ct', re.compile(r"\bjust\b \bin\b \btime\b")),
#     ('lean_ct', re.compile(r"\blean\b")),
#     ('tot_quality_mng_ct', re.compile(r"\btotal\b \bquality\b \bmanagement\b")),
#     ('six_sigm_ct', re.compile(r"\bsix\b \bsigma\b")),
#     ('scale_econ_ct', re.compile(r"\bscale\b \beconomies\b")),
#     ('scope_econ_ct', re.compile(r"\bscope\b \beconomies\b")),
#     ('econ_of_scale_ct', re.compile(r"\beconomies\b \bof\b \bscale\b")),
#     ('econ_of_scope_ct', re.compile(r"\beconomies\b \bof\b \bscope\b")),
#     ('unv_ct', re.compile(r"\buniversity\b \bof\b")),
#     ('outsource_ct', re.compile(r"\boutsource\b|\boutsourcing\b|\boutsourced\b")),
# ]
#
#
# rules = [
#     ('founded_in', re.compile(r"(.{1,30}\bfounded\b \bin\b \d{2,4}.{1,30})")),
# ]
#
#
rules = [
    ('total_words', re.compile(r"\b\w+\b")),
    ('competition_words', [re.compile(r"competitions?|competitors?|competitives?|competes?|competings?"), "(few|less|not|limited)(\s\w+){0,3}"]),
]
