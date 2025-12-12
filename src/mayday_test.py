from mayday import *

def test_lee_desastres():
    desastres = lee_desastres("data/Mayday.csv")
    print("el número total de desastres leídos es:", len(desastres))
    print("los dos primeros desastres leídos son:", desastres[:2])
    print("los dos ultimos desastres leídos son:", desastres[-2:])



def test_desastres_con_fallecidos_en_tierra():
    desastres = lee_desastres("data/Mayday.csv")
    resultado = desastres_con_fallecidos_en_tierra(desastres, 5)
    print("los cinco peores desastres con fallecidos en tierra son:", resultado)    

def test_decada_mas_colisiones():
    desastres = lee_desastres("data/Mayday.csv")
    resultado = decada_mas_colisiones(desastres)
    print("la década con más colisiones es:", resultado)




def funcion_principal():
    #test_lee_desastres()
    #test_desastres_con_fallecidos_en_tierra()
    test_decada_mas_colisiones()

if __name__ == "__main__":
    funcion_principal()
    
    

    
