def cgr (sk):
    if sk == 'cl' or sk =='c.l':
        sk = 'c.L'
    elif sk == 'cm' or sk =='c.m':
        sk = 'c.M'
    elif sk == 'ch' or sk =='c.h':
        sk = 'c.H'
    if sk == 'fl' or sk =='f.l':
        sk = 'f.L'
    elif sk == 'fm' or sk =='f.m':
        sk = 'f.M'
    elif sk == 'fh' or sk =='f.h':
        sk = 'f.H'
    if sk == 'jl' or sk =='j.l':
        sk = 'j.L'
    elif sk == 'jm' or sk =='j.m':
        sk = 'j.M'
    elif sk == 'jh' or sk =='j.h':
        sk = 'j.H'
    elif sk == 'ju' or sk =='j.u':
        sk = 'j.U'
    elif sk == 'u' or sk == 'U':
        sk == '5U'
    elif sk == 'jtr' or sk =='j.tr':
        sk = 'j.TR'
    elif sk == 'j360l' or sk =='j.360l':
        sk = 'j.360L'
    elif sk == 'j360m' or sk =='j.360m':
        sk = 'j.360M'
    elif sk == 'j360h' or sk =='j.360h':
        sk = 'j.360H'
    elif sk == 'j7u' or sk =='j.7u':
        sk = 'j.7U'
    elif sk == 'j8u' or sk =='j.8u':
        sk = 'j.8U'
    elif sk == 'j2u' or sk =='j.2u':
        sk = 'j.2U'
    elif sk == 'j6u' or sk =='j.6u':
        sk = 'j.6U'
    elif sk == 'j22l' or sk =='j.22l':
        sk = 'j.22L'
    elif sk == 'j22m' or sk =='j.22m':
        sk = 'j.22M'
    elif sk == 'j22H' or sk =='j.22h':
        sk = 'j.22H'
    elif sk == 'j236l' or sk =='j.236l':
        sk = 'j.236L'
    elif sk == 'j236m' or sk =='j.236m':
        sk = 'j.236M'
    elif sk == 'j236h' or sk =='j.236h':
        sk = 'j.236H'
    elif sk == 'j214l' or sk =='j.214l':
        sk = 'j.214L'
    elif sk == 'j214m' or sk =='j.214m':
        sk = 'j.214M'
    elif sk == 'j214h' or sk =='j.214h':
        sk = 'j.214H'
    elif sk == 'j236236h' or sk =='j.236236h':
        sk = 'j.236236H'
    elif sk == 'j236236u' or sk =='j.236236u':
        sk = 'j.236236U'
    elif sk == 'oh':
        sk = 'MH'
    
    return sk
