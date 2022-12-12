from typing import Dict, List, Tuple
from math import ceil
from bisect import bisect_right


class Chem:
    def __init__(self, name: str):
        self.name: str = name
        self.quant: int = 0
        self.source: Dict[Chem, int] = {}
        self.required_amount: int = 0
        self.residual: int = 0

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == str(other)

    def __repr__(self):
        return f"Chem({self.quant}, {self.name}) required {self.required_amount}"

    def __str(self):
        return self.name

    def claim(self, val):
        # print("claim", self.name, "for", val)
        if val <= self.residual:
            self.residual -= val
            return
        val -= self.residual
        if not self.source:
            self.required_amount += val
            return

        required_val = ceil(val/self.quant) * self.quant
        self.residual = required_val - val
        factor = required_val // self.quant
        self.required_amount += required_val
        for chem, quant in self.source.items():
            chem.claim(quant * factor)


def parse_raw_chem(raw_chem: str, all_chems: Dict[str, Chem]) -> Tuple[int, Chem]:
    quant, name = raw_chem.split(" ")
    quant = int(quant)
    return quant, all_chems.setdefault(name, Chem(name))


def read_data() -> Dict[str, Chem]:
    raw_data = """3 DJDNR => 1 ZCMR
7 VWJH => 5 ZPGT
5 BHZP => 2 DJDNR
6 KCNKC, 19 MZWS => 4 PKVJF
21 GXSHP, 1 TWGP, 3 BGCW => 1 XHRWR
12 DZGWQ, 2 XRDL, 3 XNVT => 2 FTMC
7 VWJH, 33 BGCW, 1 TBVC => 9 DSDP
1 NMTGB, 4 KCNKC, 5 SBSJ, 4 MCZDZ, 7 DLCP, 2 GRBZF, 1 CLKP, 10 VQHJG => 6 DVCR
7 ZCMR => 9 VNTF
2 VNTF, 1 GKMN => 1 TZWBH
6 QMFV, 7 GRBZF => 7 RHDZ
8 PKVJF => 9 NJQH
110 ORE => 9 GZTS
4 DJDNR, 7 SFHV => 8 KQFH
1 ZTCZ, 5 LZFBP => 7 VWPMZ
2 GKMN, 6 TZWBH, 1 GXSHP => 1 MJHJH
2 DLCP, 4 NGJRN => 3 GRBZF
2 DJDNR, 1 GSRBL => 4 VWJH
7 RMQX => 3 SFHV
1 GZTS => 7 GSRBL
3 GZTS, 1 SFHV => 3 QLXCS
10 SFHV => 3 MKTHL
2 DJDNR, 2 BGCW, 4 FSTJ => 3 GKMN
2 KQFH, 7 GSRBL => 7 TWGP
22 RHDZ, 22 DZGWQ, 2 NGJRN, 14 XHRWR, 21 VWPMZ, 15 ZPXHM, 26 BHZP => 8 BPHZ
1 QLXCS => 6 ZBTS
12 DLCP, 9 DSDP => 9 ZPXHM
1 VNTF => 5 ZBTX
2 TZWBH, 2 JCDW => 1 CPLG
1 XHRWR, 7 FSTJ, 5 DZGWQ => 4 NGJRN
179 ORE => 3 RMQX
1 DSDP => 1 MZWS
140 ORE => 8 BHZP
1 LZFBP, 4 DZGWQ => 2 PMDK
1 GZTS => 1 GXSHP
10 CPLG, 8 MCZDZ => 5 ZTCZ
5 ZPGT, 4 THLBN, 24 GSRBL, 40 VNTF, 9 DVCR, 2 SHLP, 11 PMDK, 19 BPHZ, 45 NJQH => 1 FUEL
9 MKTHL => 7 KCNKC
5 NGJRN => 3 QMFV
1 ZTCZ, 6 VNTF => 2 VQHJG
5 FTMC, 5 ZBTX, 1 MJHJH => 1 CLKP
7 FSTJ => 6 DLCP
1 DSDP => 5 KTML
4 LZFBP, 8 MKTHL => 7 MCZDZ
1 SFHV => 1 DZGWQ
2 QLXCS => 4 ZMXRH
3 KQFH, 1 DJDNR => 7 TBVC
5 DSDP => 7 THLBN
9 BHZP, 1 VWJH => 6 BGCW
4 GXSHP => 6 JCDW
1 KQFH, 3 ZMXRH => 9 XNVT
6 TBVC => 4 GVMH
3 VWPMZ, 3 GRBZF, 27 MJHJH, 2 QMFV, 4 NMTGB, 13 KTML => 7 SHLP
1 GVMH => 2 FSTJ
2 VQHJG, 2 NJQH => 8 SBSJ
1 XNVT => 2 XRDL
2 KCNKC => 5 LZFBP
2 ZBTS, 8 DLCP => 4 NMTGB"""
    raw_reactions = raw_data.split("\n")
    all_chems = {}
    for reaction in raw_reactions:
        raw_sources, raw_result = reaction.split(" => ")
        quant, result_chem = parse_raw_chem(raw_result, all_chems)
        result_chem.quant = quant
        for chem in raw_sources.split(", "):
            quant, chem = parse_raw_chem(chem, all_chems)
            result_chem.source[chem] = quant
    return all_chems


def part1():
    all_chems = read_data()
    all_chems["FUEL"].claim(1)
    print(all_chems["ORE"].required_amount)
    return all_chems["ORE"].required_amount


class FuelToORE(object):
    def __getitem__(self, item):
        all_chems = read_data()
        all_chems["FUEL"].claim(item)
        res = all_chems["ORE"].required_amount
        return res


def find_le(data, target_value, lo, hi):
    i = bisect_right(data, target_value, lo, hi)
    if i:
        return i - 1
    raise ValueError


def part2(ore_per_fuel):
    all_chems = read_data()

    total_ore = 1000000000000
    low_fuel = total_ore // ore_per_fuel
    all_chems["FUEL"].claim(low_fuel)
    low_ore = all_chems["ORE"].required_amount
    print("low_bound_fuel", low_fuel)
    print("low bound ore", low_ore)

    upper_fuel = low_fuel * 2
    all_chems = read_data()
    all_chems["FUEL"].claim(upper_fuel)
    upper_ore = all_chems["ORE"].required_amount
    print("upper_bound_fuel", upper_fuel)
    print("upper bound ore", upper_ore)

    res = find_le(FuelToORE(), total_ore, lo=low_fuel, hi=upper_fuel)
    print(res)


if __name__ == "__main__":
    ore_per_fuel = part1()
    part2(ore_per_fuel)
