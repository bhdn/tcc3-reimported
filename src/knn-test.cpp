/* a crappy k-NN implementation
 *
 * it was supposed to be a C program but turned into C++ after I noticed I
 * needed a priority queue */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>

#include <queue>
#include <vector>
#include <map>
#include <algorithm>

using namespace std;

#define ALLOC_BATCH	1024

class candidate_pair {
public:
	candidate_pair(float class__, float distance_) :
		class_(class__), distance(distance_) {}

	float class_;
	float distance;
};

class less_pair : public std::binary_function<candidate_pair*,
	candidate_pair*, bool> {
public:
        bool operator()(const candidate_pair* x,
			const candidate_pair* y) const
        {
                return x->distance < y->distance;
        }
};

float *load_examples(const char *path, size_t *found)
{
	float value;
	char discard;
	float *values = NULL;
	size_t allocated = 0;
	size_t count = 0;

	FILE *f = fopen(path, "r");
	if (!f) {
		perror(path);
		abort();
	}

	while (fscanf(f, "%f", &value) == 1) {

		if (allocated < count + 1) {
			allocated += ALLOC_BATCH;
			values = (float*) realloc(values,
					allocated * sizeof(values[0]));
			if (!values) {
				fprintf(stderr, "Oops! realloc falhou\n");
				abort();
			}
		}
		values[count++] = value;

		if (fscanf(f, "%c", &discard) != 1)
			break;
	}
	printf("readed %zu values from %s\n", count, path);

	*found = count;
	return values;
}

void test(float *trainvalues, size_t traincount, float *testvalues,
		size_t testcount, size_t windowsize, size_t k)
{
	size_t testi, traini, i;
	float powsum, dist, class_, correct_class;
	candidate_pair *candidate;
	map<float, unsigned> counter;
	map<float, unsigned>::iterator it, it2;
	float winner_class, winner_count;
	size_t correct_total = 0, total = 0;
	priority_queue<candidate_pair*, vector<candidate_pair*>, less_pair> pq;

	pq.push(new candidate_pair(0.0, 1.0));
	pq.push(new candidate_pair(0.0, 2.0));
	pq.push(new candidate_pair(0.0, 3.0));
	pq.push(new candidate_pair(0.0, 0.0));
	assert(pq.top()->distance == 3.0);

	for (testi = 0; testi < testcount; testi += windowsize + 1) {

		priority_queue<candidate_pair*,
			vector<candidate_pair*>, less_pair> pq;

		for (traini = 0; traini < traincount; traini += windowsize + 1) {

			powsum = 0.0;
			for (i = 0; i < windowsize; i++)
				powsum += powf(trainvalues[traini+i] 
						- testvalues[testi+i], 2);

			dist = sqrtf(powsum);
			class_ = trainvalues[traini+windowsize];

			assert(class_ >= 0 && class_ <= 3);
			
			if (pq.size() < k)
				pq.push(new candidate_pair(class_, dist));
			else {
				candidate = pq.top();
				if (dist < candidate->distance) {
					pq.pop();
					delete candidate;
					pq.push(new candidate_pair(class_, dist));
				}
			}
		}

		counter.clear();
		while (!pq.empty()) {
			candidate = pq.top();
			pq.pop();
			counter[candidate->class_] = 1 + counter[candidate->class_];
			delete candidate;
		}

		winner_class = -1;
		winner_count = -1;
		for (it = counter.begin() ; it != counter.end(); it++) {
			if ((*it).second > winner_count) {
				winner_count = (*it).second;
				winner_class = (*it).first;
			}
    		}
		correct_class = testvalues[testi+windowsize];

		if (correct_class == winner_class) 
			correct_total++;
		total++;
	}

	printf("total/correct: %zu/%zu\n", total, correct_total);
}

int main(int argc, char *argv[])
{
	size_t traincount, testcount, windowsize, k;

	if (argc < 5) {
		fprintf(stderr, "%s <windowsize> <k> <trainfile> "
				"<testfile>\n", argv[0]);
		return 1;
	}

	if (sscanf(argv[1], "%zu", &windowsize) != 1) {
		fprintf(stderr, "invalid window size\n");
		return 1;
	}

	if (sscanf(argv[2], "%zu", &k) != 1) {
		fprintf(stderr, "invalid number of neighbours (k)\n");
		return 1;
	}


	float *trainvalues = load_examples(argv[3], &traincount);
	float *testvalues = load_examples(argv[4], &testcount);

	test(trainvalues, traincount, testvalues, testcount, windowsize, k);

	return 0;
}
