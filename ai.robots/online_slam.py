from slam_final import *
import numpy as np


def guess_trip(data, num_landmarks, motion_noise, measurement_noise):
    print 'landmarks number: %d' %(num_landmarks)
    dim = 2* (1+num_landmarks) #2D
    Omega=np.zeros((dim,dim))
    Omega[0,0]=Omega[1,1] = 1.0

    Xi=np.zeros(dim)
    Xi[0]=Xi[1]=world_size/2.
    for k,(measurement, motion) in enumerate(data):
        for z in measurement:
            # m is landmark index in matrix
            m=2*(1+z[0])
            for b in range(2):
                Omega[b][b]     +=  1.0/measurement_noise
                Omega[m+b][m+b] +=  1.0/measurement_noise
                Omega[b][m+b]   += -1.0/measurement_noise
                Omega[m+b][b]   += -1.0/measurement_noise
                Xi[b]           += -z[1+b]/measurement_noise
                Xi[m+b]         +=  z[1+b]/measurement_noise
        
        # expand the matrix by one new position
        t = np.insert(Omega,(2,2),0, axis=0)
        Omega = np.insert(t,(2,2),0, axis=1)
        Xi = np.insert(Xi,(2,2),0, axis=0)

        # update matrix by motion from i to (i+1)
        for b in range(4):
            Omega[b][b] += 1.0/motion_noise
        for b in range(2):
            Omega[b][b+2] += -1.0/motion_noise
            Omega[b+2][b] += -1.0/motion_noise
            Xi[b]           += -motion[b]/motion_noise
            Xi[b+2]         += motion[b]/motion_noise

        # now factor out the previous pose
        A = Omega[:2,2:]
        B = Omega[:2,:2]
        C = Xi[:2]
        Omega = Omega[2:,2:] - A.T.dot(np.linalg.inv(B)).dot(A)
        Xi = Xi[2:] - A.T.dot(np.linalg.inv(B)).dot(C)

    #compute best estimate
    mu = np.linalg.inv(Omega).dot(Xi)
    return mu, Omega


def solution_check(result, answer_mu, answer_omega):
    assert len(result) == 2
    user_mu, user_omega = result
    answer_mu = answer_mu.reshape(answer_mu.size)
    assert user_mu.shape == answer_mu.shape
    assert user_omega.shape[0] == answer_omega.shape[0]
    assert np.allclose(user_mu, answer_mu)
    assert np.allclose(user_omega, answer_omega)
    print "Test case passed!"

if __name__ =="__main__":
    data = make_trip(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
    result = guess_trip(data, num_landmarks, motion_noise, measurement_noise)
    print_result(1, num_landmarks, result[0])

    data = make_trip(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
    result = guess_trip(data, num_landmarks, motion_noise, measurement_noise)
    print_result(1, num_landmarks, result[0])

"""
# -----------
# Test Case 1

testdata1          = [[[[1, 21.796713239511305, 25.32184135169971], [2, 15.067410969755826, -27.599928007267906]], [16.4522379034509, -11.372065246394495]],
                      [[[1, 6.1286996178786755, 35.70844618389858], [2, -0.7470113490937167, -17.709326161950294]], [16.4522379034509, -11.372065246394495]],
                      [[[0, 16.305692184072235, -11.72765549112342], [2, -17.49244296888888, -5.371360408288514]], [16.4522379034509, -11.372065246394495]],
                      [[[0, -0.6443452578030207, -2.542378369361001], [2, -32.17857547483552, 6.778675958806988]], [-16.66697847355152, 11.054945886894709]]]

answer_mu1         = np.array([[81.63549976607898],
                             [27.175270706192254],
                             [98.09737507003692],
                             [14.556272940621195],
                             [71.97926631050574],
                             [75.07644206765099],
                             [65.30397603859097],
                             [22.150809430682695]])

answer_omega1 = np.array([[0.36603773584905663, 0.0, -0.169811320754717, 0.0, -0.011320754716981133, 0.0, -0.1811320754716981, 0.0],
                             [0.0, 0.36603773584905663, 0.0, -0.169811320754717, 0.0, -0.011320754716981133, 0.0, -0.1811320754716981],
                             [-0.169811320754717, 0.0, 0.6509433962264151, 0.0, -0.05660377358490567, 0.0, -0.40566037735849064, 0.0],
                             [0.0, -0.169811320754717, 0.0, 0.6509433962264151, 0.0, -0.05660377358490567, 0.0, -0.40566037735849064],
                             [-0.011320754716981133, 0.0, -0.05660377358490567, 0.0, 0.6962264150943396, 0.0, -0.360377358490566, 0.0],
                             [0.0, -0.011320754716981133, 0.0, -0.05660377358490567, 0.0, 0.6962264150943396, 0.0, -0.360377358490566],
                             [-0.1811320754716981, 0.0, -0.4056603773584906, 0.0, -0.360377358490566, 0.0, 1.2339622641509433, 0.0],
                             [0.0, -0.1811320754716981, 0.0, -0.4056603773584906, 0.0, -0.360377358490566, 0.0, 1.2339622641509433]])

result = guess_trip(testdata1, 3, 2.0, 2.0)
solution_check(result, answer_mu1, answer_omega1)


# -----------
# Test Case 2

testdata2          = [[[[0, 12.637647070797396, 17.45189715769647], [1, 10.432982633935133, -25.49437383412288]], [17.232472057089492, 10.150955955063045]],
                      [[[0, -4.104607680013634, 11.41471295488775], [1, -2.6421937245699176, -30.500310738397154]], [17.232472057089492, 10.150955955063045]],
                      [[[0, -27.157759429499166, -1.9907376178358271], [1, -23.19841267128686, -43.2248146183254]], [-17.10510363812527, 10.364141523975523]],
                      [[[0, -2.7880265859173763, -16.41914969572965], [1, -3.6771540967943794, -54.29943770172535]], [-17.10510363812527, 10.364141523975523]],
                      [[[0, 10.844236516370763, -27.19190207903398], [1, 14.728670653019343, -63.53743222490458]], [14.192077112147086, -14.09201714598981]]]

answer_mu2         = np.array([[63.37479912250136],
                             [78.17644539069596],
                             [61.33207502170053],
                             [67.10699675357239],
                             [62.57455560221361],
                             [27.042758786080363]])

answer_omega2      = np.array([[0.22871751620895048, 0.0, -0.11351536555795691, 0.0, -0.11351536555795691, 0.0],
                             [0.0, 0.22871751620895048, 0.0, -0.11351536555795691, 0.0, -0.11351536555795691],
                             [-0.11351536555795691, 0.0, 0.7867205207948973, 0.0, -0.46327947920510265, 0.0],
                             [0.0, -0.11351536555795691, 0.0, 0.7867205207948973, 0.0, -0.46327947920510265],
                             [-0.11351536555795691, 0.0, -0.46327947920510265, 0.0, 0.7867205207948973, 0.0],
                             [0.0, -0.11351536555795691, 0.0, -0.46327947920510265, 0.0, 0.7867205207948973]])

result = guess_trip(testdata2, 2, 3.0, 4.0)
solution_check(result, answer_mu2, answer_omega2)
"""
