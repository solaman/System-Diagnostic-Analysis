# System-Diagnostic-Analysis
How to run: python Dedekind.py <br />
type "-help" to see a list of all available commands <br />
This project is meant to be used either as a command line, console, or library. <br />
If you wish create the monotone boolean functions and .dot files for each, try
running "python Dedekind.py" and use the command line or console. <br />
Else, all of these functions are available through Model.DedekindLattice.py . Which also have useful
features for System Diagnostic Analysis: <br />
by instantiated an instance of DedekindLattice.py, you can call "getNextNode()" which will return <br />
a new monotone boolean function within the DedekindLattice. From here, you can then call "isConsistent", passing
 in a configuration, to see if the function would accept it. <br />
 DO NOT BE CONFUSED BY computeALLMIS and the "isConsistent" function of DedekindNodes! <br />
 In System-Diagnostic-Analysis, when we ask for a minimal inconsistent subset, we ask for 
 the smallest set which explains the inconsistency of an input to an answer. <br />
 When we ask if a set "isConsistent" however, we are asking if the set explains the inConsistency
 of the input to an answer (would assuming the set is erroneous make the answer consistent with the input?).

