// Aravind Krishnan Varadarajan


#include <iostream>
#include "Vtop.h"
#include "Vtop__Syms.h"
#include <fstream>
#include <string>

using namespace std;


int main (){

	long int c,compare,size, i,j,k;
	float b=0;
	c=0;
	i=0;
	k=0;
	ifstream infile;
	ofstream ofile;
	Vtop circuit;
	infile.open("lev_vec.vec");
	ofile.open("coverage_cycle.trace");
	
	int total_pts;
	total_pts = circuit.num_branch_cov_pts();
	
	int cov_count[total_pts];
	for(int i =0; i < total_pts ; i++)
	    cov_count[i] = 0;
	
	infile >> size;       // get size
	j=size;
	char content[j];
	vector<bool> bb (j,0); // declaring requiered variable to pass i/p from file to circuit.
	
	circuit.sim_init(); // initializing circuit
	circuit.eval();
	
	while ( infile >> content )   // while not EOF read
	{
		if(content[0] != 'E' ){       // If not END then
		for(k=0;k<j;k++)
		{
			bb[k]=content[k]-'0';      // parse i/p
		}
		circuit.set_input_with_reset(bb);  // set i/p
		circuit.eval();                    //eval
		circuit.toggle_clock();            // toggle clock to 1
		circuit.eval();                    //eval
		circuit.toggle_clock();            // toggle clock to 0
		circuit.eval();                    // eval
	    c = 0;
	    while ( c < total_pts)
	    {
	        //cout << "Coverage count of pt : " << c << " is " << circuit.get_cov_pt_value(c) << ".\n";
	        //cout << "Count of pt : " << c << " is " << cov_count[c] << ".\n";
	        if(circuit.get_cov_pt_value(c)>cov_count[c])
	        {
	             cov_count[c] = circuit.get_cov_pt_value(c);
	             ofile << c << ",";
	        }
	        c++;
	    }
	    ofile << "\n";
	
		}
	        //cout << " I am here 2 \n";
	}
	
	return 0;

}


