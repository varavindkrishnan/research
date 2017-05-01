// -*-c++-*-
#ifndef __DYNAMIC_LOADER_H
#define __DYNAMIC_LOADER_H

#include "VerilatedCircuit.h"
#include <dlfcn.h>
#include <iostream>

using namespace std;

//this is realistically a wrapper to a C api via a struct.
//Due to this, we allocate and deallocate manually, forcing
//the user to track the lifespan of the loaded library.
//
//If there were more time, I would do this as a more controlled
//production evironment where the dynamicLoader class itself
//is responsible for the lifecycle.
//
//Additional caveat, verilator has some severe limitations
//that cause this to largely be a hack. First, multiple
//simulation units are not supported, hence the can_instantiate
//boolean and the circuit_ref. If the user mishandles, we can
//attempt to detect and throw an error, or multiple accidental calls
//can always return the same circuit reference.
//
//To handle this, we carry a single reference to the library
//and validate it.
class DynamicCircuitLoader {
private:
    static bool can_instantiate;
    static VerilatedCircuit* circuit_ref;
    static void* dyn_lib;
public:
    static VerilatedCircuit* createCircuit(string);
    static bool cleanupCircuit(VerilatedCircuit*);
    static bool validateCircuit(VerilatedCircuit*);
};

#endif
