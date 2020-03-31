from Beam  import Beam

class Context():

    def __init__(self, strategy: Beam) -> None:
        self._strategy= strategy

    def doYourThing(self):
        print("This moment of Inertia is: ", self._strategy.I)
        print("The first natural bending frequency is: ",  self._strategy.fn)
