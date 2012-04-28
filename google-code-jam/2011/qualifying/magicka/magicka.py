import sys

class ElementList:
    def __init__(self, combo_map, opp_map):
        self.list      = []
        self.elements  = {}
        self.combo_map = combo_map
        self.opp_map   = opp_map

    def append(self, element):
        if not self.list:
            self.list.append(element)
            if element not in self.elements:
                self.elements[element] = 1
            else:
                self.elements[element] += 1
            return

        combined = self.list[-1] + element
        if combined in self.combo_map:
            popped = self.list.pop(-1)
            self.elements[popped] -= 1
            combined_result = self.combo_map[combined]
            self.list.append(combined_result)
            if combined_result not in self.elements:
                self.elements[combined_result] = 1
            else:
                self.elements[combined_result] += 1
            return

        if element not in self.opp_map:
            self.list.append(element)
            if element not in self.elements:
                self.elements[element] = 1
            else:
                self.elements[element] += 1
            return

        opp_elements = self.opp_map[element]
        clear = False
        for opp in opp_elements:
            if opp in self.elements and self.elements[opp] > 0:
                self.list = []
                self.elements = {}
                clear = True
                break
        if not clear:
            self.list.append(element)
            if element not in self.elements:
                self.elements[element] = 1
            else:
                self.elements[element] += 1

def invoke(input_str):
    input_list = input_str.strip().split()

    num_combos = int(input_list.pop(0))
    combo_map = {}

    for i in range(0, num_combos):
        combo_str = input_list.pop(0)
        combo_map[combo_str[0:2]] = combo_str[2]
        combo_map[combo_str[0:2][::-1]] = combo_str[2]

    num_opps = int(input_list.pop(0))
    opp_map = {}

    for i in range(0, num_opps):
        opp_str = input_list.pop(0)
        if opp_str[0] not in opp_map:
            opp_map[opp_str[0]] = [opp_str[1]]
        else:
            opp_map[opp_str[0]].append(opp_str[1])
        if opp_str[1] not in opp_map:
            opp_map[opp_str[1]] = [opp_str[0]]
        else:
            opp_map[opp_str[1]].append(opp_str[0])

    num_elements = int(input_list.pop(0))
    element_list = list(input_list.pop(0))
    element_list_out = ElementList(combo_map, opp_map)

    for element in element_list:
        element_list_out.append(element)

    return str(element_list_out.list).replace("'", "")

if len(sys.argv) != 2:
    print "Usage: python %s INPUT_FILE" % (sys.argv[0])
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = [l.strip() for l in f.readlines()]
    num_cases = int(lines[0])
    for i,case in enumerate(lines[1:num_cases+1]):
        print "Case #%d: %s" % (i+1, invoke(case))

