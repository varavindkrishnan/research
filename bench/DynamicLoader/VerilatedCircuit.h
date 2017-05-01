// -*-c++-*-
#ifndef __VERILATEDCIRCUIT_H
#define __VERILATEDCIRCUIT_H

#include <vector>
#include <string>
#include <cstdint>
#include <iostream>
#include <verilatedos.h>
#include <boost/multiprecision/cpp_int.hpp>
using namespace std;

//forward declare

class DynamicCircuitLoader;

typedef vluint8_t     ByteData;
typedef vluint16_t    WordData;
typedef vluint32_t    DWordData;
typedef vluint64_t    QWordData;
typedef vluint32_t*   PackedWordDataArr;
typedef boost::multiprecision::int256_t PackedWordData;

typedef union ByteAlignedData {
    ByteData b_data;
    WordData w_data;
    DWordData dw_data;
    QWordData qw_data;
    ByteData*  b_data_ptr;
    WordData*  w_data_ptr;
    DWordData* dw_data_ptr;
    QWordData* qw_data_ptr;
    PackedWordData w_sel_data;
    PackedWordDataArr* w_sel_data_ptr;
    ByteAlignedData() {}
};

struct vsim_value {
    //16 bytes POD(even with custom constructor), easy to copy (basically free).
    //Only a few are ever in existence at one time.
    //Saves the allocation and deallocation utilized
    //by the vpi by allowing direct access into the
    //simulator, via pointer.
    uint32_t type; //4 bytes
    uint32_t width; //4 bytes
    ByteAlignedData data; //8 bytes (64-bit pointers, QWord data)
    vsim_value() {} //random initialization
    vsim_value(uint32_t t, uint32_t w, uint64_t val) : type(t), width(w) {
        switch(type) {
        case 0:
            data.b_data = (ByteData)val;
            break;
        case 1:
            data.w_data = (WordData)val;
            break;
        case 2:
            data.dw_data = (DWordData)val;
            break;
        case 3:
            data.qw_data = (QWordData)val;
            break;
        }
    }
    vsim_value(uint32_t t, uint32_t w, PackedWordData val) : type(t), width(w) {
	data.w_sel_data = (PackedWordData)val; 
	}

    vsim_value(const vsim_value &temp) {
        type = temp.type;
        width = temp.width;
        switch(temp.type) {
        case 0:
            data.b_data = temp.data.b_data;
            break;
        case 1:
            data.w_data = temp.data.w_data;
            break;
        case 2:
            data.dw_data = temp.data.dw_data;
            break;
        case 3:
            data.qw_data = temp.data.qw_data;
            break;
        case 4:
            data.b_data_ptr = temp.data.b_data_ptr;
            break;
        case 5:
            data.w_data_ptr = temp.data.w_data_ptr;
            break;
        case 6:
            data.dw_data_ptr = temp.data.dw_data_ptr;
            break;
        case 7:
            data.qw_data_ptr = temp.data.qw_data_ptr;
            break;
        case 8:
            data.w_sel_data = temp.data.w_sel_data;
            break;
        case 9:
            data.w_sel_data_ptr = temp.data.w_sel_data_ptr;
            break;
        }
    }

    inline uint64_t get_val() {
        if(type == 0) return ((uint64_t) data.b_data) & 0xff;
        else if(type == 1) return ((uint64_t) data.w_data) & 0xffff;
        else if(type == 2) return ((uint64_t) data.dw_data) & 0xffffffff;
        else if(type == 3) return ((uint64_t) data.qw_data) & 0xffffffffffffffff;
        else return 0;
    }

	inline PackedWordData get_wide_val() {
		return data.w_sel_data;
	}
};

enum class Timescale : char {
    PICOSECOND = 0,
    NANOSECOND,
    MICROSECOND,
    MILLISECOND
};

struct simple_data {
    uint32_t type;
    uint32_t width;
    ByteAlignedData data;
	simple_data() {}
    simple_data(const simple_data &temp) {
        type = temp.type;
        width = temp.width;
        switch(temp.type) {
        case 0:
            data.b_data = temp.data.b_data;
            break;
        case 1:
            data.w_data = temp.data.w_data;
            break;
        case 2:
            data.dw_data = temp.data.dw_data;
            break;
        case 3:
            data.qw_data = temp.data.qw_data;
            break;
        case 4:
            data.b_data_ptr = temp.data.b_data_ptr;
            break;
        case 5:
            data.w_data_ptr = temp.data.w_data_ptr;
            break;
        case 6:
            data.dw_data_ptr = temp.data.dw_data_ptr;
            break;
        case 7:
            data.qw_data_ptr = temp.data.qw_data_ptr;
            break;
        case 8:
            data.w_sel_data = temp.data.w_sel_data;
            break;
        case 9:
            data.w_sel_data_ptr = temp.data.w_sel_data_ptr;
            break;
        }
    }
};

class verilator_state {
public:
    void * state;
    uint32_t ant_index_; // which ant
    uint32_t round_index_; // which round
    uint32_t cycle_index_; // which cycle
    uint32_t data_base_index_; // index in the data base for vectors
    int branch_reached_; // the state that reach the branch
    double true_ph_; // the path true_ph of the current state from true_ph function
};

struct Wave {
    Timescale ts;
    uint32_t period;
    uint8_t duty_cycle; //255 = 100%
};

struct VerilatedCircuit {
    friend class DynamicCircuitLoader;
private:
    const char* (*var_get_name_nostl)(uint32_t) = nullptr;
    const char* (*dump_out_nostl)() = nullptr;
    const char* (*op_cov_file_nostl)() = nullptr;
    simple_data (*var_get_val_pod)(uint32_t) = nullptr;
    uint32_t (*var_get_id_nostl)(const char*) = nullptr;
public:
    //CORE SIM IO FUNCTIONS
    void (*random_vec_in)(vector<bool>&) = nullptr;
    void (*random_vec_in_with_reset)(vector<bool>&) = nullptr;
    uint32_t (*num_input_bits)() = nullptr;
    uint32_t (*num_input_bits_reset)() = nullptr;
    void (*set_input) (vector<bool>) = nullptr;
    void (*set_input_with_reset) (vector<bool>) = nullptr;
    void (*sim_init_clock) () = nullptr;
    void (*sim_reset_clock) () = nullptr;
    bool (*start_sim) () = nullptr;
    bool (*low_clock) () = nullptr;
    void (*toggle_clock) () = nullptr; //TODO: MULTIPLE CLOCK DOMAINS
    verilator_state (*get_state)(uint32_t, uint32_t, uint32_t, uint32_t, int, double) = nullptr;
    //void (*restore_state)(verilator_state&) = nullptr;
    uint32_t (*get_num_var)() = nullptr;
    uint32_t (*var_get_width)(uint32_t) = nullptr;
    bool (*var_is_array)(uint32_t) = nullptr;

    uint32_t (*num_branch_cov_pts)() = nullptr;
    uint32_t (*num_toggle_cov_pts)() = nullptr;
    void (*clear_coverage)() = nullptr;
    uint32_t (*get_cov_pt_value)(uint32_t) = nullptr;
	uint32_t (*num_assert_pts)() = nullptr;
	uint32_t (*num_cov_pts)() = nullptr;
	void (*get_branches_with_assert)(vector<int> &) = nullptr;

    //timescale functions for alternate simulation with time increments
    void (*setup_clock_waveform) (Wave&) = nullptr;
    void (*circuit_eval) () = nullptr;
    Timescale (*get_timescale) () = nullptr;
    void (*set_timescale) (Timescale&) = nullptr;
    void (*inc_time) () = nullptr;
    uint64_t (*get_time) () = nullptr;
    void (*reset_time)() = nullptr;

    //Verilator setup
    void (*sim_init) () = nullptr;
    void (*sim_delete) () = nullptr;
    //Callback bindings
    void (*register_comb_monitor)( void (*method_ptr)(uint32_t) ) = nullptr;
    void (*register_seq_monitor) ( void (*method_ptr)(uint32_t, uint32_t) ) = nullptr;
    void (*subscribe)(uint32_t) = nullptr;
    void (*unsubscribe)() = nullptr;

    //lev file bindings
    void (*get_lev)(const vector <vector<bool> >&, vector<vector<bool> >&) = nullptr;
    void (*reset_lev)(vector<vector<bool> >&) = nullptr;
    bool (*is_excluded_branch)() = nullptr;

    //verilated stuff
    bool (*verilated_finish)() = nullptr;

    //stl_wrappers
    string var_get_name(uint32_t);
    void dump_out(ostream& os);
    string op_cov_file();
    vsim_value var_get_val(uint32_t);
    uint32_t var_get_id(string);
};

#endif
