#include <verilated_dpi.h>
#include "VerilatedCircuit.h"

extern "C" {
    void (*callback_combo_monitor)(uint32_t) = nullptr;
    void (*callback_seq_monitor)(uint32_t, uint32_t) = nullptr;

    void assign_monitor (IData monitor_id, uint32_t observer_id) {
        if(callback_seq_monitor != nullptr)
            callback_seq_monitor(observer_id, monitor_id);
    }
    void nosen_wire_monitor (uint32_t observer_id) {
        if(callback_combo_monitor != nullptr)
            callback_combo_monitor(observer_id);
    }
}
