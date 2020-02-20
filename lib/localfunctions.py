from cqc.pythonLib import CQCConnection, qubit
import random

#onewayfunction

def one_way_function(host, BB84_key, db_id, r, M):
    q = qubit(host)

    BB84_key = int(BB84_key, 2)
    owf_key = bin(BB84_key)[2:] + bin(db_id)[2:] + bin(r)[2:] + bin(M)[2:]
    owf_key = int(abs(hash(str(owf_key))))
    # p1 , p2, p3 are sorted in a list of prime numbers , differents, so coprimes 
    # thus rotation X(key%p1) and Y(key%p2) and Z(key%p3) are independant
    listpn=[1000008439,1000008487,	1000008511,	1000008557,	1000008593,	1000008617,	1000008637,	1000008649,	1000008661,	1000008671,	1000008679,1000008719,	1000008727,	1000008761,	1000008773,	1000008791,	1000008797,	1000008803,	1000008811,	1000008829,	1000008853,1000008899,	1000008917,	1000008937,	1000008967,	1000009009,	1000009013,	1000009063,	1000009081,	1000009093,	1000009099,1000009123,	1000009133,	1000009163,	1000009183,	1000009211,	1000009223,	1000009259,	1000009277,	1000009279,	1000009289,1000009301,	1000009321,	1000009331,	1000009363,	1000009399,	1000009403,	1000009421,	1000009441,	1000009457,	1000009469,1000009487,	1000009519,	1000009529,	1000009531,	1000009541,	1000009559,	1000009561,	1000009567,	1000009573,	1000009579,1000009597,	1000009601,	1000009609,	1000009631,	1000009651,	1000009667,	1000009679,	1000009711,	1000009733,	1000009739,1000009757,	1000009789,	1000009831,	1000009859,	1000009867,	1000009961,	1000009999,	1000010029,	1000010051,	1000010069,1000010101,	1000010153,	1000010173,	1000010189,	1000010197,	1000010233,	1000010243,	1000010251,	1000010267,	1000010281,1000010303,	1000010321,	1000010327,	1000010351,	1000010357,	1000010381,	1000010449,	1000010467,	1000010483,	1000010503,1000010513,	1000010549,	1000010593,	1000010597,	1000010611,	1000010633,	1000010659,	1000010699,	1000010707,	1000010723,1000010747,	1000010749,	1000010761,	1000010773,	1000010777,	1000010801,	1000010833,	1000010903,	1000010953,	1000010969,1000010971,	1000010981,	1000010987,	1000011007,	1000011011,	1000011071,	1000011083,	1000011091,	1000011107,	1000011109,1000011137,	1000011149,	1000011161,	1000011223,	1000011239,	1000011253,	1000011269,	1000011277,	1000011283,	1000011289,1000011301,	1000011317,	1000011329,	1000011371,	1000011377,	1000011391,	1000011421,	1000011479,	1000011487,	1000011497,1000011517,	1000011533,	1000011539,	1000011559,	1000011583,	1000011601,	1000011619,	1000011631,	1000011659,	1000011673,1000011679,	1000011707,	1000011763,	1000011767,	1000011769,	1000011773,	1000011799,	1000011811,	1000011821,	1000011823,1000011847,	1000011869,	1000011967,	1000011983,	1000011989,	1000012019,	1000012037,	1000012121,	1000012157,	1000012177,1000012187,	1000012217,	1000012219,	1000012231,	1000012241,	1000012253,	1000012297,	1000012309,	1000012333,	1000012337]
    size = len(listpn)-1
    p1 = listpn[random.randint(0,size)]
    p2 = listpn[random.randint(0,size)]
    while p2==p1:
        p2 = listpn[random.randint(0,size)]
    p3 = listpn[random.randint(0,size)]
    while p3==p1 or p3==p2:
        p3 = listpn[random.randint(0,size)]
    q.rot_X(owf_key%p1%256)
    q.rot_Y(owf_key%p2%256)
    q.rot_Z(owf_key%p3%256)
    return q

    
#swaptest

def T(q):
    # T = RZ(pi/4) * e(i*pi/8)
    q.rot_Z(256//8)
    return


def invT(q):
    # T* == RZ(-pi/4) * e(i*pi/8)
    q.rot_Z(256 - 256//8)
    return


def CSWAP(q0, q1, q2):
    # fredkin implementation from :
    # https://www.mathstat.dal.ca/~selinger/quipper/doc/QuipperLib-GateDecompositions.html
    q2.cnot(q1)
    q2.H()
    T(q0)
    T(q1)
    T(q2)
    q1.cnot(q0)
    q2.cnot(q1)
    q0.cnot(q2)
    invT(q1)
    T(q2)
    q0.cnot(q1)
    invT(q0)
    invT(q1)
    q2.cnot(q1)
    q0.cnot(q2)
    q1.cnot(q0)
    q2.H()
    q2.cnot(q1)
    return


def swap(conn, q1, q2):
    # swap_test implementation from :
    # https://en.wikipedia.org/wiki/Swap_test

    q0 = qubit(conn)
    q0.H()
    CSWAP(q0, q1, q2)
    q0.H()
    m = q0.measure()

    q1.measure()
    q2.measure()
           
    return m


def swap_test(host,q1,q2): 
    BB84_key = "10"
    db_id = 1
    M = 2
    res_same = []
    res_diff = []
    for i in range(10):
        salt = random.randint(0, 1000)
        epsilon = random.randint(1,10)
        q1 = one_way_function(host, BB84_key, db_id, salt, M)
        q2 = one_way_function(host, BB84_key, db_id, salt, M)
        m_same = swap(host, q1,q2)
        """q1 = one_way_function(SWAP, BB84_key, db_id, salt, M)
        q2 = one_way_function(SWAP, BB84_key, db_id, salt + epsilon, M)
        m_diff = swap(SWAP, q1,q2)"""
        res_same.append(m_same)
        #res_diff.append(m_diff)
    score_same = sum(res_same)/len(res_same)
    #score_diff = sum(res_diff)/len(res_diff)
    print('swap test score for identical state', score_same)
    # print('swap test score for different state', score_diff)
    """if score_same!=1:
        return 0
    else
        return 1"""

if __name__ == "__main__":
    with CQCConnection("Alice") as Alice:
        q1 = qubit(Alice)
        q2 = qubit(Alice)
        swap_test(Alice,q1,q2)