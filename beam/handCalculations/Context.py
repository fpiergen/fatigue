from beam  import Beam

class Context():

    def __init__(self, strategy: Beam) -> None:
        self._strategy= strategy

    def doYourThing(self):
        print("This moment of Inertia is: ", float(round(self._strategy.I,3)))
        print("The first natural bending frequency is: ", float(round(self._strategy.fn,3)))
        #print("The max stress is: ",  float(round(self._strategy.maxStress,3)))


    @property
    def strategy(self) -> Beam:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Beam) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """
        self._strategy = strategy

#    def firstNaturalFrequency(self):

# Put a setter to set a different strategy in this class
