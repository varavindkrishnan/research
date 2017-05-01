#include "DynamicCircuitLoader.h"

bool DynamicCircuitLoader::can_instantiate = true;
VerilatedCircuit* DynamicCircuitLoader::circuit_ref = nullptr;
void* DynamicCircuitLoader::dyn_lib = nullptr;

VerilatedCircuit* DynamicCircuitLoader::createCircuit(string library_path) {
    if((can_instantiate) && (circuit_ref == nullptr)) {
        dyn_lib = dlopen(library_path.c_str(), RTLD_LAZY);
        if(dyn_lib == nullptr) {
            cerr << "LIBRARY LOAD FAILURE" << endl;    //load fail
            return nullptr;
        }

        can_instantiate = false;
        circuit_ref = new VerilatedCircuit();

        circuit_ref->random_vec_in = (void (*)(vector<bool>&)) dlsym(dyn_lib, "random_vec_in");
        if(circuit_ref->random_vec_in == nullptr) {
            cerr << "Load failure: random_vec_in" << endl;
        }

        circuit_ref->random_vec_in_with_reset = (void(*)(vector<bool>&)) dlsym(dyn_lib, "random_vec_in_with_reset");
        if(circuit_ref->random_vec_in_with_reset == nullptr) {
            cerr << "Load failure: random_vec_in_with_reset" << endl;
        }

        circuit_ref->num_input_bits = (uint32_t (*)()) dlsym(dyn_lib, "num_input_bits");
        if(circuit_ref->num_input_bits == nullptr) {
            cerr << "Load failure: num_input_bits" << endl;
        }

        circuit_ref->num_input_bits_reset = (uint32_t (*)()) dlsym(dyn_lib, "num_input_bits_reset");
        if(circuit_ref->num_input_bits == nullptr) {
            cerr << "Load failure: num_input_bits_reset" << endl;
        }

        circuit_ref->set_input = (void(*)(vector<bool>)) dlsym(dyn_lib, "set_input");
        if(circuit_ref->set_input == nullptr) {
            cerr << "Load failure: set_input" << endl;
        }

        circuit_ref->set_input_with_reset = (void(*)(vector<bool>)) dlsym(dyn_lib, "set_input_with_reset");
        if(circuit_ref->set_input_with_reset == nullptr) {
            cerr << "Load failure: set_input_with_reset" << endl;
        }

        circuit_ref->sim_init_clock = (void(*)()) dlsym(dyn_lib, "sim_init_clock");
        if(circuit_ref->sim_init_clock == nullptr) {
            cerr << "Load failure: sim_init_clock" << endl;
        }

        circuit_ref->sim_reset_clock = (void(*)()) dlsym(dyn_lib, "sim_reset_clock");
        if(circuit_ref->sim_reset_clock == nullptr) {
            cerr << "Load failure: sim_reset_clock" << endl;
        }

        circuit_ref->start_sim = (bool (*)()) dlsym(dyn_lib, "start_sim");
        if(circuit_ref->start_sim == nullptr) {
            cerr << "Load failure: start_sim" << endl;
        }

        circuit_ref->low_clock = (bool (*)()) dlsym(dyn_lib, "low_clock");
        if(circuit_ref->low_clock == nullptr) {
            cerr << "Load failure: low_clock" << endl;
        }

        circuit_ref->toggle_clock = (void (*)()) dlsym(dyn_lib, "toggle_clock");
        if(circuit_ref->toggle_clock == nullptr) {
            cerr << "Load failure: toggle_clock" << endl;
        }

        circuit_ref->get_state = (verilator_state (*)(uint32_t, uint32_t, uint32_t, uint32_t, int, double)) dlsym(dyn_lib, "get_state");
        if(circuit_ref->get_state == nullptr) {
            cerr << "Load failure: get_state" << endl;
        }

        /*circuit_ref->restore_state = (void (*)(verilator_state&)) dlsym(dyn_lib, "restore_state");
        if(circuit_ref->restore_state == nullptr) {
            cerr << "Load failure: restore_state" << endl;
        }*/

        circuit_ref->get_num_var = (uint32_t (*)()) dlsym(dyn_lib, "get_num_var");
        if(circuit_ref->get_num_var == nullptr) {
            cerr << "Load failure: get_num_var" << endl;
        }

        circuit_ref->var_get_name_nostl = (const char* (*)(uint32_t)) dlsym(dyn_lib, "var_get_name");
        if(circuit_ref->var_get_name_nostl == nullptr) {
            cerr << "Load failure: var_get_name" << endl;
        }

        circuit_ref->var_get_width = (uint32_t (*)(uint32_t)) dlsym(dyn_lib, "var_get_width");
        if(circuit_ref->var_get_width == nullptr) {
            cerr << "Load failure: var_get_width" << endl;
        }

        circuit_ref->var_is_array = (bool (*)(uint32_t)) dlsym(dyn_lib, "var_is_array");
        if(circuit_ref->var_is_array == nullptr) {
            cerr << "Load failure: var_is_array" << endl;
        }

        circuit_ref->var_get_id_nostl = (uint32_t (*)(const char*)) dlsym(dyn_lib, "var_get_id");
        if(circuit_ref->var_get_id_nostl == nullptr) {
            cerr << "Load failure: var_get_id" << endl;
        }

        circuit_ref->var_get_val_pod = (simple_data (*)(uint32_t)) dlsym(dyn_lib, "var_get_val");
        if(circuit_ref->var_get_val_pod == nullptr) {
            cerr << "Load failure: var_get_val" << endl;
        }

        circuit_ref->num_branch_cov_pts = (uint32_t (*)()) dlsym(dyn_lib, "num_branch_cov_pts");
        if(circuit_ref->num_branch_cov_pts == nullptr) {
            cerr << "Load failure: num_branch_cov_pts" << endl;
        }

        circuit_ref->num_toggle_cov_pts = (uint32_t (*)()) dlsym(dyn_lib, "num_toggle_cov_pts");
        if(circuit_ref->num_toggle_cov_pts == nullptr) {
            cerr << "Load failure: num_toggle_cov_pts" << endl;
        }

        circuit_ref->get_cov_pt_value = (uint32_t (*)(uint32_t)) dlsym(dyn_lib, "get_cov_pt_value");
        if(circuit_ref->get_cov_pt_value == nullptr) {
            cerr << "Load failure: get_cov_pt_value" << endl;
        }

        circuit_ref->op_cov_file_nostl = (const char* (*)()) dlsym(dyn_lib, "op_cov_file");
        if(circuit_ref->op_cov_file_nostl == nullptr) {
            cerr << "Load failure: op_cov_file" << endl;
        }

        circuit_ref->dump_out_nostl = (const char* (*)()) dlsym(dyn_lib, "dump_out");
        if(circuit_ref->dump_out_nostl == nullptr) {
            cerr << "Load failure: dump_out" << endl;
        }

        circuit_ref->setup_clock_waveform = (void (*)(Wave&)) dlsym(dyn_lib, "setup_clock_waveform");
        if(circuit_ref->setup_clock_waveform == nullptr) {
            cerr << "Load failure: setup_clock_waveform" << endl;
        }

        circuit_ref->circuit_eval = (void (*)()) dlsym(dyn_lib, "circuit_eval");
        if(circuit_ref->circuit_eval == nullptr) {
            cerr << "Load failure: circuit_eval" << endl;
        }

        circuit_ref->get_timescale = (Timescale (*)()) dlsym(dyn_lib, "get_timescale");
        if(circuit_ref->get_timescale == nullptr) {
            cerr << "Load failure: get_timescale" << endl;
        }

        circuit_ref->set_timescale = (void (*)(Timescale&)) dlsym(dyn_lib, "set_timescale");
        if(circuit_ref->set_timescale == nullptr) {
            cerr << "Load failure: set_timescale" << endl;
        }

        circuit_ref->inc_time = (void (*)()) dlsym(dyn_lib, "inc_time");
        if(circuit_ref->inc_time == nullptr) {
            cerr << "Load failure: inc_time" << endl;
        }

        circuit_ref->get_time = (uint64_t (*)()) dlsym(dyn_lib, "get_time");
        if(circuit_ref->get_time == nullptr) {
            cerr << "Load failure: get_time" << endl;
        }

        circuit_ref->reset_time = (void (*)()) dlsym(dyn_lib, "reset_time");
        if(circuit_ref->reset_time == nullptr) {
            cerr << "Load failure: reset_time" << endl;
        }

        circuit_ref->sim_init = (void (*)()) dlsym(dyn_lib, "sim_init");
        if(circuit_ref->sim_init == nullptr) {
            cerr << "Load failure: sim_init" << endl;
        }

        circuit_ref->sim_delete = (void (*)()) dlsym(dyn_lib, "sim_delete");
        if(circuit_ref->sim_delete == nullptr) {
            cerr << "Load failure: sim_delete" << endl;
        }

        circuit_ref->register_comb_monitor = (void (*)(void (*)(uint32_t))) dlsym(dyn_lib, "register_comb_monitor");
        if(circuit_ref->register_comb_monitor == nullptr) {
            cerr << "Load failure: register_comb_monitor" << endl;
        }

        circuit_ref->register_seq_monitor = (void (*)(void (*)(uint32_t, uint32_t))) dlsym(dyn_lib, "register_seq_monitor");
        if(circuit_ref->register_seq_monitor == nullptr) {
            cerr << "Load failure: register_seq_monitor" << endl;
        }

        circuit_ref->subscribe = (void (*)(uint32_t)) dlsym(dyn_lib, "subscribe");
        if(circuit_ref->subscribe == nullptr) {
            cerr << "Load failure: subscribe" << endl;
        }

        circuit_ref->unsubscribe = (void (*)()) dlsym(dyn_lib, "unsubscribe");
        if(circuit_ref->unsubscribe == nullptr) {
            cerr << "Load failure: unsubscribe" << endl;
        }

        circuit_ref->get_lev = (void (*)(const vector <vector<bool> >&, vector<vector<bool> >&)) dlsym(dyn_lib, "get_lev");
        if(circuit_ref->get_lev == nullptr) {
            cerr << "Load failure: get_lev" << endl;
        }

        circuit_ref->reset_lev = ( void (*)(vector<vector<bool> >&)) dlsym(dyn_lib, "reset_lev");
        if(circuit_ref->reset_lev == nullptr) {
            cerr << "Load failure: reset_lev" << endl;
        }

        circuit_ref->is_excluded_branch = (bool (*)()) dlsym(dyn_lib, "is_excluded_branch");
        if(circuit_ref->is_excluded_branch == nullptr) {
            cerr << "Load failure: is_excluded_branch" << endl;
        }

        circuit_ref->verilated_finish = (bool (*)()) dlsym(dyn_lib, "verilated_finish");
        if(circuit_ref->verilated_finish == nullptr) {
            cerr << "Load failure: verilated_finish" << endl;
        }

        circuit_ref->clear_coverage = (void (*)()) dlsym(dyn_lib, "clear_coverage");
        if(circuit_ref->clear_coverage == nullptr) {
            cerr << "Load failure: clear_coverage" << endl;
        }

        circuit_ref->num_cov_pts = (uint32_t (*)()) dlsym(dyn_lib, "num_cov_pts");
        if(circuit_ref->num_cov_pts == nullptr) {
            cerr << "Load failure: num_cov_pts" << endl;
        }

        circuit_ref->get_branches_with_assert = (void (*)(vector<int>&)) dlsym(dyn_lib, "get_branches_with_assert");
        if(circuit_ref->get_branches_with_assert == nullptr) {
            cerr << "Load failure: num_cov_pts" << endl;
        }

        return circuit_ref;
    }
    return nullptr;
}

bool DynamicCircuitLoader::cleanupCircuit(VerilatedCircuit* ckt) {
    if((!can_instantiate) && (circuit_ref == ckt) && (ckt!= nullptr)) {
        delete ckt;
        can_instantiate = true;
        circuit_ref = nullptr;
        dlclose(dyn_lib);
        return true;
    } else {//don't delete things we don't own
        return false;
    }
}

bool DynamicCircuitLoader::validateCircuit(VerilatedCircuit* ckt) {
    return (ckt == circuit_ref) && (!can_instantiate);
}


string VerilatedCircuit::var_get_name(uint32_t id) {
    return string(var_get_name_nostl(id));
}

uint32_t VerilatedCircuit::var_get_id(string name) {
    return var_get_id_nostl(name.c_str());
}

void VerilatedCircuit::dump_out(ostream& os) {
    os << string(dump_out_nostl()) << endl;
}
string VerilatedCircuit::op_cov_file() {
    return string(op_cov_file_nostl());
}


vsim_value VerilatedCircuit::var_get_val(uint32_t id) {
    simple_data data = var_get_val_pod(id);
	cout << " var_get_val " << id << " width " << data.width << " type " << data.type << endl;
    vsim_value ret;
    ret.type = data.type;
    ret.width = data.width;
    switch(data.type) {
    case 0:
        ret.data.b_data = data.data.b_data;
        break;
    case 1:
        ret.data.w_data = data.data.w_data;
        break;
    case 2:
        ret.data.dw_data = data.data.dw_data;
        break;
    case 3:
        ret.data.qw_data = data.data.qw_data;
        break;
	case 4:
		ret.data.b_data_ptr = data.data.b_data_ptr;
		break;
    case 5:
        ret.data.w_data_ptr = data.data.w_data_ptr;
        break;
	case 6:
		ret.data.dw_data_ptr = data.data.dw_data_ptr;
		break;
    case 7:
        ret.data.qw_data_ptr = data.data.qw_data_ptr;
        break;
    case 8:
        ret.data.w_sel_data = data.data.w_sel_data;
        break;
    case 9:
        ret.data.w_sel_data_ptr = data.data.w_sel_data_ptr;
        break;
    }
    //ret.data = data.data;
    return ret;
}

#ifdef __DYNLIBTEST
int main (int argc, char* []) {
    VerilatedCircuit * test;
    test = DynamicCircuitLoader::createCircuit("./serial_lpfSim.so");
    DynamicCircuitLoader::cleanupCircuit(test);
}
#endif

