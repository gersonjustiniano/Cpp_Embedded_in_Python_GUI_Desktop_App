#include<pybind11/pybind11.h>
#include<pybind11/stl.h>
#include<pybind11/numpy.h>
#include<iostream>
#include<string>
#include<chrono>
#include<ctime>
#include<sstream>
#include<iomanip>
#include<random>
#include<algorithm>
#include<vector>

using namespace std;
using std::string;
namespace py=pybind11;

struct initial_data {
	float initial_range;
	float final_range;
	float initial_random;
	float final_random;
	float spread;
	int precision;
};
vector<initial_data> symbol_data(string symbol) {
	if (symbol=="EURUSD") {
		return {{1.0f, 1.2f, 0.0001f, 0.0002f, 0.0001f, 5}};
	} else if (symbol=="BTCUSD") {
		return {{90000.0f, 100000.0f, 0.0001f, 0.0002f, 50.0f, 2}};
	} else if (symbol=="XAUUSD") {
		return {{3000.0f, 3500.0f, 0.0001f, 0.0002f, 1.0f, 3}};
	} else if (symbol=="US500") {
		return {{5000.0f, 5500.0f, 0.0001f, 0.0002f, 0.5f, 2}};
	} else {
		return {};
	}
}

void get_data(string symbol,py::dict var, py::object initial_datetime,int fr) {

	auto data=symbol_data(symbol);
	auto d=data[0];

	string t;
	py::list col=var["time"].cast<py::list>();
	size_t size_col=col.size();

	py::list tick_lst=var["tick_time"].cast<py::list>();
	size_t tick_size=tick_lst.size();

	py::list bid_lst=var["bid"].cast<py::list>();
	py::list ask_lst=var["ask"].cast<py::list>();
	size_t bid_size=bid_lst.size();

	//GET DATETIME:

	if (size_col<fr+1) {
		py::module_ datetime=py::module_::import("datetime");
		py::object timedelta=datetime.attr("timedelta");
		py::object new_datetime=initial_datetime+timedelta(py::arg("seconds")=tick_size);
		py::object formatted = new_datetime.attr("strftime")("%Y-%m-%d %H:%M:%S.%f");
        t = py::str(formatted).cast<string>();
        t = t.substr(0, t.size() - 3);
	} else {	
		auto now=chrono::system_clock::now();
		time_t tc = chrono::system_clock::to_time_t(now);
        tm* local_tm = localtime(&tc);
        auto duration = now.time_since_epoch();
        auto millis = chrono::duration_cast<chrono::milliseconds>(duration).count() % 1000;

        ostringstream oss;
        oss << put_time(local_tm, "%Y-%m-%d %H:%M:%S");
        oss << '.' << setfill('0') << setw(3) << millis;
        t = oss.str();
	}
	tick_lst.append(t);

	//GET RANDOM PRICES:
	
	random_device rd;
	mt19937 gen(rd());
	float spread=d.spread,bid,ask;
	if (bid_size==0) {
		uniform_real_distribution<> float_dist1(d.initial_range,d.final_range);
		double r_float=float_dist1(gen);
		ostringstream oss;
		oss<<fixed<<setprecision(d.precision)<<r_float;
		string float_random=oss.str();
		bid=stof(float_random);
		ask=bid+spread;
		bid_lst.append(bid);
		ask_lst.append(ask);
	} else {
		uniform_real_distribution<> float_dist2(d.initial_random,d.final_random);
		double r=float_dist2(gen);
		double last_bid=bid_lst[bid_size-1].cast<double>();
		double b1=last_bid*(1+r);
		double b2=last_bid*(1-r);
		uniform_real_distribution<> float_dist(b2,b1);
		double bid_float=float_dist(gen);
		ostringstream oss;
		oss<<fixed<<setprecision(d.precision)<<bid_float;
		string float_random=oss.str();
		bid=stof(float_random);
		ask=bid+spread;
		bid_lst.append(bid);
		ask_lst.append(ask);
	}		
}

vector<string> split(string str, char delimeter) {
	stringstream ss(str);
	string item;
	vector<string> parts;
	while (getline(ss,item,delimeter)) {
		parts.push_back(item);
	}
	return parts;
}

string order_data(py::dict var, string interval) {

	string val,m1,m2,h1,h2,d1,d2;
	py::list tick=var["tick_time"].cast<py::list>();
	size_t tick_size=tick.size();
	
	if (tick_size>=2) {
		m1=split(split(tick[tick_size-1].cast<string>(),' ')[1],':')[1];
		m2=split(split(tick[tick_size-2].cast<string>(),' ')[1],':')[1];
		h1=split(split(tick[tick_size-1].cast<string>(),' ')[1],':')[0];
		h2=split(split(tick[tick_size-2].cast<string>(),' ')[1],':')[0];
		d1=split(split(tick[tick_size-1].cast<string>(),' ')[0],'-')[2];
		d2=split(split(tick[tick_size-2].cast<string>(),' ')[0],'-')[2];

		if (interval=="M1") {
			if (m1!=m2) {
				val="nc";
			} else {
				val=" ";
			}
		} else if (interval=="M5" || interval=="M15" || interval=="M30") {
			int t_int=stoi(interval.substr(1));
			int m1_int=stoi(m1);
			int m2_int=stoi(m2);
			vector<int> minutes1;
			vector<int> minutes2;
			for (int i=m2_int;i<m1_int+1;i++) {
				minutes1.push_back(i%t_int);
			}
			for (int i=m2_int;i<m1_int+60;i++) {
				minutes2.push_back(i%t_int);
			}
			if ((m1!=m2 && m1_int%t_int==0) || 
				(m1_int%t_int!=0 && m2_int%t_int!=0 && m1_int>m2_int && find(minutes1.begin(),minutes1.end(),0)!=minutes1.end()) ||
				(m1_int%t_int!=0 && m2_int%t_int!=0 && m1_int<m2_int && find(minutes2.begin(),minutes2.end(),0)!=minutes2.end())) {
				val="nc";
			} else {
				val=" ";
			}
		} else if (interval=="H1") {
			if (h1!=h2) {
				val="nc";
			} else {
				val=" ";
			}
		} else if (interval=="H4") {
			int int_h1=stoi(h1);
			if (h1!=h2 && int_h1%4==0) {
				val="nc";
			} else {
				val=" ";
			}
		} else if (interval=="D1") {
			if (d1!=d2) {
				val="nc";
			} else {
				val=" ";
			}
		}

	} else {
		val="i";
	}

	return val;
}

void candles(py::dict var, string val) {
	py::list tick_lst=var["tick_time"].cast<py::list>();
	py::list bid_lst=var["bid"].cast<py::list>();
	py::list time_lst=var["time"].cast<py::list>();
	py::list open_lst=var["open"].cast<py::list>();
	py::list high_lst=var["high"].cast<py::list>();
	py::list low_lst=var["low"].cast<py::list>();
	py::list close_lst=var["close"].cast<py::list>();
	size_t tick_size=tick_lst.size()-1;
	size_t bid_size=bid_lst.size()-1;
	size_t high_size=high_lst.size()-1;
	size_t low_size=low_lst.size()-1;
	size_t close_size=close_lst.size()-1;

	if (val=="i" || val=="nc") {
		time_lst.append(tick_lst[tick_size]);
		open_lst.append(bid_lst[bid_size]);
		high_lst.append(bid_lst[bid_size]);
		low_lst.append(bid_lst[bid_size]);
		close_lst.append(bid_lst[bid_size]);
	} else if (val==" ") {
		double bid=bid_lst[bid_size].cast<double>();
		double high=high_lst[high_size].cast<double>();
		double low=low_lst[low_size].cast<double>();

		if (bid>high) {
			high_lst[high_size]=bid;
		} else if (bid<low) {
			low_lst[low_size]=bid;
		}
		close_lst[close_size]=bid;
	}
}

double double_sma(int n, py::list p1_lst, py::list p2_lst, py::list time_lst) {
	
	size_t time_size=time_lst.size();
	double sum=0.0;

	for (int i=0;i<n;i++) {
		double price1=p1_lst[time_size-i-1].cast<double>();
		double price2=p2_lst[time_size-i-1].cast<double>();
		sum+=(price1+price2)/2;
	}
	return sum/static_cast<double>(n);	
}

double smma(int n, py::list lst, py::list p1_lst, py::list p2_lst, py::dict var, string val) {
	
	py::list time_lst=var["time"].cast<py::list>();
	size_t time_size=time_lst.size();
	size_t pos1=time_size-1;
	size_t pos2=time_size-2;


	int lst0=lst[0].cast<int>();
	int lst1=lst[1].cast<int>();
	int lst2=lst[2].cast<int>();

	unordered_map<int,string> gator_map={
		{lst[0].cast<int>(),"lips"},
		{lst[1].cast<int>(),"teeth"},
		{lst[2].cast<int>(),"jaw"}
	};

	py::list gator=var[py::str(gator_map[n])].cast<py::list>();

	size_t gator_size=gator.size();
	size_t gator_idx=(val=="nc") ? gator_size-1 : gator_size-2;

	double prev_gator=gator[gator_idx].cast<double>();
	double price1=p1_lst[pos1].cast<double>();
	double price2=p2_lst[pos1].cast<double>();
	
	return (prev_gator*(n-1)+(price1+price2)/2)/static_cast<double>(n);

}

void alligator(py::list lst, string p1, string p2, py::dict var, string val) {
	
	double croc_smma;
	py::module_ np = py::module_::import("numpy");

	py::list p1_lst=var[py::str(p1)].cast<py::list>();
	py::list p2_lst=var[py::str(p2)].cast<py::list>();
	py::list time_lst=var["time"].cast<py::list>();
	size_t time_size=time_lst.size();
	size_t pos=time_size-1;

	int lst0=lst[0].cast<int>();
	int lst1=lst[1].cast<int>();
	int lst2=lst[2].cast<int>();
	
	for (auto n_obj:lst) {
		int n=n_obj.cast<int>();

		if (time_size == static_cast<size_t>(n)) {
			croc_smma=double_sma(n,p1_lst,p2_lst,time_lst);
		} else if (time_size > static_cast<size_t>(n)) {
			croc_smma=smma(n,lst,p1_lst,p2_lst,var,val);
		} else if (time_size < static_cast<size_t>(n)) {
			//croc_smma=py::float_(np.attr("nan"));
			croc_smma=numeric_limits<double>::quiet_NaN();
		}

		if (val=="nc") {
			if (n==lst0) {
				var["lips"].cast<py::list>().append(croc_smma);
			} else if (n==lst1) {
				var["teeth"].cast<py::list>().append(croc_smma);
			} else if (n==lst2) {
				var["jaw"].cast<py::list>().append(croc_smma);
			}
		} else if (val==" ") {
			if (n==lst0) {
				var["lips"].cast<py::list>()[pos]=croc_smma;
			} else if (n==lst1) {
				var["teeth"].cast<py::list>()[pos]=croc_smma;
			} else if (n==lst2) {
				var["jaw"].cast<py::list>()[pos]=croc_smma;
			}
		} else if (val=="i") {
			if (n==lst0) {
				var["lips"].cast<py::list>().append(numeric_limits<double>::quiet_NaN());
			} else if (n==lst1) {
				var["teeth"].cast<py::list>().append(numeric_limits<double>::quiet_NaN());
			} else if (n==lst2) {
				var["jaw"].cast<py::list>().append(numeric_limits<double>::quiet_NaN());
			}
		}
	}
}

void fractals(int n, py::dict var, string val) {

	py::list time_lst=var["time"].cast<py::list>();
	size_t time_size=time_lst.size();

	py::list high_lst=var["high"].cast<py::list>();
	py::list low_lst=var["low"].cast<py::list>();

	if (val=="nc" && time_size>=static_cast<size_t>(2*n+1)) {
		
		bool up=true;
		bool down=true;

		size_t mid=time_size-n-1;
		double mid_high=high_lst[mid].cast<double>();
		double mid_low=low_lst[mid].cast<double>();

		for (int i=0;i<n;i++) {
			size_t idx_left=mid-i-1;
			size_t idx_right=mid+i+1;

			if (mid_high<high_lst[idx_left].cast<double>() || mid_high<high_lst[idx_right].cast<double>()) {
				up=false;
			}
			if (mid_low>low_lst[idx_left].cast<double>() || mid_low>low_lst[idx_right].cast<double>()) {
				down=false;
			}
		}
		
		if (up) {
			py::list up_val;
			up_val.append(time_lst[mid]);
			up_val.append(high_lst[mid]);
			var["up"].cast<py::list>().append(up_val);
		} else if (down) {
			py::list down_val;
			down_val.append(time_lst[mid]);
			down_val.append(low_lst[mid]);
			var["down"].cast<py::list>().append(down_val);
		}
	}
}

void awesome(py::list lst, string q1, string q2, py::dict var, string val) {
	
	//SMAS:
	
	double avg_ao;
	py::list q1_lst=var[py::str(q1)].cast<py::list>();
	py::list q2_lst=var[py::str(q2)].cast<py::list>();
	py::list time_lst=var["time"].cast<py::list>();
	size_t time_size=time_lst.size();
	size_t pos=time_size-1;

	int lst0=lst[0].cast<int>();
	int lst1=lst[1].cast<int>();

	for(auto n_obj:lst) {
		int n=n_obj.cast<int>();

		if (time_size>=static_cast<size_t>(n)) {
			avg_ao=double_sma(n,q1_lst,q2_lst,time_lst);
		} else if (time_size<static_cast<size_t>(n)) {
			avg_ao=0.0;
		}

		if (val=="nc" || val=="i") {
			if (n==lst0) {
				var["fast_ao"].cast<py::list>().append(avg_ao);
			} else if (n==lst1) {
				var["slow_ao"].cast<py::list>().append(avg_ao);
			}
		} else if (val==" ") {
			if (n==lst0) {
				var["fast_ao"].cast<py::list>()[pos]=avg_ao;
			} else if (n==lst1) {
				var["slow_ao"].cast<py::list>()[pos]=avg_ao;
			}
		}
	}

	//AWESOME:
	
	double ao;
	size_t q1_size=q1_lst.size();
	
	if (q1_size>=static_cast<size_t>(lst1)) {
		double fast_ao=var["fast_ao"].cast<py::list>()[pos].cast<double>();
		double slow_ao=var["slow_ao"].cast<py::list>()[pos].cast<double>();
		ao=fast_ao-slow_ao;
	} else if (q1_size<static_cast<size_t>(lst1)) {
		ao=0.0;
	}

	if (val=="nc" || val=="i") {
		var["ao"].cast<py::list>().append(ao);
	} else if (val==" ") {
		var["ao"].cast<py::list>()[pos]=ao;
	}
	
}

PYBIND11_MODULE(indicator,m) {
	m.def("get_data",&get_data);
	m.def("order_data",&order_data);
	m.def("candles",&candles);
	m.def("alligator",&alligator);
	m.def("fractals",&fractals);
	m.def("awesome",&awesome);
}
