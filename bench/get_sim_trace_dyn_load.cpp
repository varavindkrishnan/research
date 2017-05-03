// Aravind Krishnan Varadarajan


#include <iostream>
#include <fstream>
#include <string>
#include "./DynamicLoader/DynamicCircuitLoader.h"
#include "./DynamicLoader/VerilatedCircuit.h"
#define CIRCUIT_NAME_LEN 1024
#define MODE 1 // the default mode, enable faulty/fault free simulation together

using namespace std;

class read_in_parameters {
public:
    char cktName[CIRCUIT_NAME_LEN];
    unsigned int seed;

    int mode; // fault free & faulty simulation together. default: 1, enabled
    int n_stride;
    int property;
    int rand_synch;
    string libpath;
    string config;
    int n_vec = 0;
    int n_cover = 1;
    int n_assert_cover = 1;
    int address_var;
    bool mem_vec = false;
	bool op_cov = false;
    read_in_parameters(void):
        seed(0),
        mode(MODE),
        property(0),
        config("beacon.config") {}
    ~read_in_parameters(void) { }

    void parse_parameters(int argc,char *argv[]);
    void scanone(int argc, char *argv[], int i, int *varptr);
    void scanones(int argc, char *argv[], int i, char *varptr);
    void scanonef(int argc, char *argv[], int i, float *varptr);
    void print_parameters(void);
    void read_config_file(char* config_file);
};


int main (int argc, char **argv, char **env){

    read_in_parameters paras;
	paras.parse_parameters(argc, argv);
    //cout << "PARSING PARAMS" << endl;
    paras.parse_parameters(argc, argv);

    if (0 && argc && argv && env) {} // Prevent unused variable warnings

	VerilatedCircuit* top;
    top = DynamicCircuitLoader::createCircuit(paras.libpath);

	//cout << "Completed loading circuit \n";
    top->sim_init();
	//cout << "Circuit instantiated \n";


	long int c,compare,size, i,j,k;
	float b=0;
	c=0;
	i=0;
	k=0;
	ifstream infile;
	ofstream ofile;
	infile.open("/home/arkrish/research/my_work/git/research/bench/lev_vec.vec");
	ofile.open("/home/arkrish/research/my_work/git/research/bench/coverage_cycle.trace");
	
	int total_pts;
	total_pts = top->num_branch_cov_pts();
	
	int cov_count[total_pts];
	for(int i =0; i < total_pts ; i++)
	    cov_count[i] = 0;
	
	infile >> size;       // get size
	j=size;
	char content[j];
	vector<bool> bb (j,0); // declaring requiered variable to pass i/p from file to top->
	
	top->sim_init(); // initializing circuit
	top->sim_init_clock(); // initializing circuit
	
	while ( infile >> content )   // while not EOF read
	{
		if(content[0] != 'E' ){       // If not END then
		for(k=0;k<j;k++)
		{
			bb[k]=content[k]-'0';      // parse i/p
		}
		top->set_input_with_reset(bb);  // set i/p
		top->toggle_clock();            // toggle clock to 1
		top->circuit_eval();                    //eval
		top->toggle_clock();            // toggle clock to 0
		top->circuit_eval();                    // eval
	    c = 0;
	    while ( c < total_pts)
	    {
	        if(top->get_cov_pt_value(c)>cov_count[c])
	        {
	             cov_count[c] = top->get_cov_pt_value(c);
	             ofile << c << ",";
	        }
	        c++;
	    }
	    ofile << "\n";
	
		}
	}
	
	return 0;

}

void read_in_parameters::parse_parameters(int argc,char *argv[]) {
    int i;
    int temp;
    char path[256];

    if (argc < 2) {
        fprintf(stderr, "Usage: %s -libpath <path> <ckt>\n", argv[0]);
        exit(-1);
    }

    for (i=1; i < argc; i++) {
        if (argv[i][0] != '-') { // circuit name
            strcpy(this->cktName, argv[i]);
        } else if (strcmp(argv[i],"-seed") == 0) { // seed
            scanone(argc,argv,++i,&temp);
            this->seed = (unsigned int)temp;
        } else if (strcmp(argv[i],"-m") == 0 && i<argc-1) { // mode, two together
            scanone(argc,argv,++i,&temp);
            this->mode = temp;
        } else if (strcmp(argv[i],"-prp") == 0 && i<argc-1) { // property
            scanone(argc,argv,++i,&temp);
            this->property = temp;
        } else if(strcmp(argv[i], "-nsim") == 0 && i<argc-1) {
            scanone(argc, argv, ++i, &temp);
            this->n_vec = temp;
        } else if(strcmp(argv[i], "-rs") == 0 && i<argc-1) {
            scanone(argc, argv, ++i, &temp);
            this->rand_synch = temp;
            cout << "SET RAND_SYNCH to " << temp << endl;
        } else if(strcmp(argv[i], "-libpath") == 0 && i<argc-1) {
            scanones(argc, argv, ++i, path);
            this->libpath = path;
        } else if(strcmp(argv[i], "-ncov") == 0 && i<argc-1) {
            scanone(argc, argv, ++i, &temp);
            this->n_cover = temp;
        } else if(strcmp(argv[i], "-mem") == 0 && i<argc-1) {
            scanone(argc, argv, ++i, &temp);
            this->address_var = temp;
			this->mem_vec = true;
		} else if(strcmp(argv[i], "-nassertcov") == 0 && i<argc-1) {
			scanone(argc, argv, ++i, &temp);
			this->n_assert_cover = temp;
		} else if(strcmp(argv[i], "-op_cov") == 0) {
			this->op_cov = true;
		}
        else {
            fprintf(stderr, "General parameters:\n");
            fprintf(stderr, "  -seed N = set up seed number with integer N\n");
            fprintf(stderr, "  -m N = set the mode number with integer N\n");
            fprintf(stderr, "  -prp N = set the the property with integer N\n");
            fprintf(stderr, "  -rs N = 0 for random synch off 1 for on\n");
            fprintf(stderr, "  -ncov N = set the threshold coverage for each point(default 1)\n");
            fprintf(stderr, "  -mem N = use addressable vector, N is the output port variable id used for addressing.");
            exit(-1);
        }
    }
}

void read_in_parameters::scanone(int argc, char *argv[], int i, int *varptr) {
    if (i>=argc || sscanf(argv[i],"%i",varptr)!=1) {
        fprintf(stderr, "Bad argument %s\n", i<argc ? argv[i] : argv[argc-1]);
        exit(-1);
    }
}

void read_in_parameters::scanones(int argc, char *argv[], int i, char *varptr) {
    if (i>=argc || sscanf(argv[i],"%s",varptr)!=1) {
        fprintf(stderr, "Bad argument %s\n", i<argc ? argv[i] : argv[argc-1]);
        exit(-1);
    }
}

void read_in_parameters::scanonef(int argc, char *argv[], int i, float *varptr) {
    if (i>=argc || sscanf(argv[i],"%f",varptr)!=1) {
        fprintf(stderr, "Bad argument %s\n", i<argc ? argv[i] : argv[argc-1]);
        exit(-1);
    }
}

void read_in_parameters::print_parameters(void) {
    cout << "circuit name is " << this->cktName << endl;
    cout << "seed using is " << this->seed << endl;
    cout << "mode is " << this->mode << endl;
    cout << "property is " << this->property << endl;
}



