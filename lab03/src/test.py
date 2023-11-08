from twist_generator import TwistGenerator

gen = TwistGenerator()
gen.SetW(4)
gen.start(2)
for i in range(40):
    print(gen.Next())