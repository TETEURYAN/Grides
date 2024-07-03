#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
#include "ortools/sat/cp_model.h"
 
using namespace std;
const int N1 = (int)2e5 + 100;
#define DEBUG false
#define db(x)  \
    if (DEBUG) \
    cout << #x << ": " << x << endl
#define PI 3.14159265358979323846264338327
#define forn for(int i=0;i<n;i++)
#define forj for(int j=0;j<n;j++)
#define fornn for(int i=1;i<=n;i++)
#define fornj for(int j=1;j<=n;j++)
#define each(i,c) for(__typeof((c).begin()) i=(c).begin(),i##_end=(c).end();i!=i##_end;++i)
#define all(x) (x).begin(), (x).end()
#define sz(a) (int)(a.size())
#define lower(x) for(auto & i : x) i = tolower(i, locale());
#define mem(a,b) memset((a),(b),sizeof(a))
#define f first
#define s second
#define pb push_back
#define pp pop_back
#define mp make_pair
#define yes cout<<"Yes"<<'\n';
#define no  cout<<"No"<<'\n';
#define one  cout<<-1<<'\n';
#define nl  '\n';
 
typedef __gnu_pbds::tree<int, __gnu_pbds::null_type, less<int>, __gnu_pbds::rb_tree_tag, __gnu_pbds::tree_order_statistics_node_update> ordered_set;
typedef long long ll;
typedef set<ll> si;
typedef set<char> sc;
typedef vector<ll> vi;
typedef priority_queue<ll> pri;
typedef vector<char> vc;
typedef pair<ll,ll> pi;
typedef vector<pi>	vpi;
typedef vector<vi>	vvi;
typedef vector<vc>	vvc;
typedef vector<string> vs;
typedef vector<bool> vb;
const long long M = 1e9+7;
#define N  10000005
#define lli unsigned long long int
#define ll long long

using namespace operations_research;
using namespace sat;
using namespace std;

map<string, pair<vector<string>, vector<int>>> GetData(const string& arquivo) {
    ifstream infile(arquivo);
    map<string, pair<vector<string>, vector<int>>> dados;
    string linha;
    while (getline(infile, linha)) {
        istringstream iss(linha);
        string professor, disciplina;
        int horario;
        iss >> professor;
        vector<string> disciplinas;
        vector<int> horarios_disponiveis;
        while (iss >> disciplina >> horario) {
            disciplinas.push_back(disciplina);
            horarios_disponiveis.push_back(horario);
        }
        dados[professor] = make_pair(disciplinas, horarios_disponiveis);
    }
    return dados;
}
signed main(){
        	
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    map<string, pair<vector<string>, vector<int>>> dados_professores = GetData("ex01.txt");

    map<string, vector<string>> turmas = {
        {"T1", {"Mat1", "Mat2", "Mat3"}},
        {"T2", {"Mat1", "Mat4", "Mat5"}},
        {"T3", {"Mat2", "Mat3", "Mat5"}}
    };

    CpModelBuilder model;

    map<tuple<string, string, int>, BoolVar> x;
    for (const auto& turma : turmas) {
        for (const auto& materia : turma.second) {
            for (int horario = 1; horario <= 3; ++horario) {
                x[{turma.first, materia, horario}] = model.NewBoolVar();
            }
        }
    }

    for (const auto& [professor, disciplinas_horarios] : dados_professores) {
        const auto& [disciplinas, horarios_disponiveis] = disciplinas_horarios;
        for (size_t i = 0; i < disciplinas.size(); ++i) {
            const auto& disciplina = disciplinas[i];
            const auto& horarios = horarios_disponiveis[i];
            for (const auto& turma : turmas) {
                if (find(turma.second.begin(), turma.second.end(), disciplina) != turma.second.end()) {
                    LinearExpr sum;
                    for (int horario : horarios) {
                        sum += x[{turma.first, disciplina, horario}];
                    }
                    model.AddEquality(sum, 1);
                }
            }
        }
    }

    for (const auto& turma : turmas) {
        for (int horario = 1; horario <= 3; ++horario) {
            LinearExpr sum;
            for (const auto& materia : turma.second) {
                sum += x[{turma.first, materia, horario}];
            }
            model.AddLessOrEqual(sum, 1);
        }
    }

    CpSolver solver;
    const CpSolverResponse response = solver.Solve(model.Build());

    if (response.status() == CpSolverStatus::OPTIMAL || response.status() == CpSolverStatus::FEASIBLE) {
        for (const auto& turma : turmas) {
            cout << "Turma " << turma.first << ":\n";
            for (const auto& materia : turma.second) {
                for (int horario = 1; horario <= 3; ++horario) {
                    if (solver.Value(x[{turma.first, materia, horario}])) {
                        cout << "  Matéria " << materia << ": Horário " << horario << "\n";
                    }
                }
            }
        }
    } else {
        cout << "Nenhuma solução encontrada.\n";
    }

    return 0;


}