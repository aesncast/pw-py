#!/usr/bin/env python3
# compability_tests:
# contains tests to make sure compatible passwords for
# old pw versions can be generated.

from pw.transform import bad_legacy1, bad_legacy2

def legacy1_test():
    assert(bad_legacy1('','','') == '56wHhmaODaDwK2K9BPRf\n')
    assert(bad_legacy1('','a','a') == 'muanOrnvE48mmYEgkG0v\n')
    assert(bad_legacy1('','a','b') == 'Z4OjHqv2jMwGYPk1wIJi\n')
    assert(bad_legacy1('','b','b') == 'xTxqrE7jaNpabaXDlUWd\n')
    assert(bad_legacy1('','c','c') == 'Z1xnYm11s8etfKyjZqKd\n')
    assert(bad_legacy1('','abc','abc') == 'CgVRIX6ldLbfKkqVrZYj\n')
    assert(bad_legacy1('','abc','ghi') == 'rsuF1zJBBwGExgRhDJ1Z\n')
    assert(bad_legacy1('','key','domain') == 'k9Dz6RwfbTTZtxnJjcEs\n')
    assert(bad_legacy1('','1','1') == '1rWRXEYFe8sAX0b2Qz32\n')
    assert(bad_legacy1('','1','2') == 'ZzrusIz7sAuR5ePGC1uj\n')
    assert(bad_legacy1('','4','5') == 'WiPpahIxLEFVUBPtKltA\n')
    assert(bad_legacy1('','7','8') == 'E5OsgOaaiZHOpKg8aGq5\n')
    assert(bad_legacy1('','0','0') == 'rHI2ilhqGMGQiDk1c84D\n')
    assert(bad_legacy1('','hello','world') == '3IC9zV0iNYUkJO73PN9x\n')
    assert(bad_legacy1('','A','A') == '7DfeWaSLAaFCKAlHI5Db\n')
    assert(bad_legacy1('','A','B') == 'WjPhXdhK2m9wJdGX1UTb\n')
    assert(bad_legacy1('','B','B') == '1rerUY8E0SrFM9EKWgUM\n')
    assert(bad_legacy1('','C','C') == '9iN6b0aHIyumBIFHEg8o\n')
    assert(bad_legacy1('','ABC','ABC') == 'aR0JOEcL3ECwE2lDd56e\n')
    assert(bad_legacy1('','ABC','GHI') == 'weZzLLb58aPQ5pu1bx5a\n')
    assert(bad_legacy1('','KEY','DOMAIN') == 'kZIqKxTpHxC3xOyKmY5f\n')
    assert(bad_legacy1('','1','1') == '1rWRXEYFe8sAX0b2Qz32\n')
    assert(bad_legacy1('','1','2') == 'ZzrusIz7sAuR5ePGC1uj\n')
    assert(bad_legacy1('','4','5') == 'WiPpahIxLEFVUBPtKltA\n')
    assert(bad_legacy1('','7','8') == 'E5OsgOaaiZHOpKg8aGq5\n')
    assert(bad_legacy1('','0','0') == 'rHI2ilhqGMGQiDk1c84D\n')
    assert(bad_legacy1('','HELLO','WORLD') == '7SXIEu79irCkCih1qLyp\n')
    

def legacy2_test():
    assert(bad_legacy2('','','','') == '6Xucw!MHuL?Gaa8 x9sR\n')
    assert(bad_legacy2('','a','a','a') == 'AMSy4DCEWBPMvJE53pRh\n')
    assert(bad_legacy2('','a','b','c') == 'nXuBC482PBPFxxaxbgPK\n')
    assert(bad_legacy2('','b','b','b') == 'Za7ddHuw8zmyGthzNTrN\n')
    assert(bad_legacy2('','c','c','c') == 'yTPv4xEWdqPRrhtVX2GP\n')
    assert(bad_legacy2('','abc','abc','abc') == 'BgKch!YutD?MhjB Q4uc\n')
    assert(bad_legacy2('','abc','ghi','def') == 'EVQJY4;M8pYr!e7PNd?P\n')
    assert(bad_legacy2('','key','domain','user') == 'GwsBsNnW5j6nhMrRh3E5\n')
    assert(bad_legacy2('','1','1','1') == '25zhGBX8Uf,xTapMVSGf\n')
    assert(bad_legacy2('','1','2','3') == 'dBr3qrjjNy,NcpQ4hWpg\n')
    assert(bad_legacy2('','4','5','6') == 'Kf6aB!fRun?UEDL bC8U\n')
    assert(bad_legacy2('','7','8','9') == 'QWk2dXNKNr,bgPndUpEQ\n')
    assert(bad_legacy2('','0','0','0') == 'PTjy364VzXQ5rrfhCYvx\n')
    assert(bad_legacy2('','hello','world','!') == 'fqCCvPrSKQyvTuEFK4XG\n')
    assert(bad_legacy2('','A','A','A') == 'tc8X3pr4eQ,y27aWhTKu\n')
    assert(bad_legacy2('','A','B','C') == 'yDXLU!uFZC?gwRL MY7G\n')
    assert(bad_legacy2('','B','B','B') == 'fDVyJyWYav292tKt9jE4\n')
    assert(bad_legacy2('','C','C','C') == '3EbDShRREb,ny7Rm6ZuT\n')
    assert(bad_legacy2('','ABC','ABC','ABC') == 'qwVJhr;qMRCQ!ZeUuE?D\n')
    assert(bad_legacy2('','ABC','GHI','DEF') == 'U3JYTjHkrv,r5PTyPAbA\n')
    assert(bad_legacy2('','KEY','DOMAIN','USER') == 'Nx5SmnMXnCxstx9uUmyd\n')
    assert(bad_legacy2('','1','1','1') == '25zhGBX8Uf,xTapMVSGf\n')
    assert(bad_legacy2('','1','2','3') == 'dBr3qrjjNy,NcpQ4hWpg\n')
    assert(bad_legacy2('','4','5','6') == 'Kf6aB!fRun?UEDL bC8U\n')
    assert(bad_legacy2('','7','8','9') == 'QWk2dXNKNr,bgPndUpEQ\n')
    assert(bad_legacy2('','0','0','0') == 'PTjy364VzXQ5rrfhCYvx\n')
    assert(bad_legacy2('','HELLO','WORLD','!') == 'V7ApH!6Aeh?Mmue 4na9\n')

    
def run_tests():
    legacy1_test()
    legacy2_test()
    print("all compatibility tests passed")


if __name__ == "__main__":
    run_tests()
