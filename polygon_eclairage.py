# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 21:44:36 2021

@author: hugob
"""

from shared import point_classe, segment_classe,\
    intersection_demi_droite_segment, dist,\
    point_egaux, point_appartient_segment, determinant_3_points, signe

# Taille des point affichés sur le canvas
size = 4


class polygon_eclairage():
    """Docstring"""

    def __init__(self, start_point, polygon, canvas, mode_demo=False):
        """Arguments :
            - start_point : Tuple ou liste sous la forme (x, y) ou [x, y]
            - polygon : Liste de sommets sous la forme  [(xA, yA), (xB, yB)...]
            - canvas : Canvas de dessin
            - mode_demo : Boolean, True pour activer le mode de démonstration
        Retourne le polygon d'éclairage sous la forme d'une liste de points
        au format tuple : [(xA, yA), (xB, yB) ...]"""

        if not (type(start_point) == tuple or type(start_point) == list):
            return None
        if not (len(start_point) == 2):
            return None

        self.canvas, self.mode_demo = canvas, mode_demo

        self.canvas.delete("demo")

        # Création d'une liste contenant les segments du polygon
        self.liste_segments_polygon = list()
        A = point_classe(polygon[0][0], polygon[0][1])
        for i in range(1, len(polygon)):
            B = point_classe(polygon[i][0], polygon[i][1])
            self.liste_segments_polygon.append(segment_classe(A, B))
            A = B
        B = point_classe(polygon[0][0], polygon[0][1])
        self.liste_segments_polygon.append(segment_classe(A, B))

        # Création d'une liste contenant les sommets du polygon
        self.liste_sommets_polygon = list()
        for point in polygon:
            self.liste_sommets_polygon.append(point_classe(point[0], point[1]))

        # Le point O est le point où l'on souhaite connaître le polygon
        # d'éclairage
        self.O = point_classe(start_point[0], start_point[1])

        if self.mode_demo:
            # Affichage de la source lumineuse en jaune
            self.canvas.create_oval(self.O.x-size, self.O.y-size,
                                    self.O.x+size, self.O.y+size,
                                    fill='white', tag='demo')

    def return_polygon(self):
        # Liste qui contiendra les intersections retenues (la plus proche
        # du point et les projections) avec leur status
        liste_intersections_def = list()

        # Pour chaque sommet du polygon, on va chercher son projeté le plus
        # proche
        for sommet in self.liste_sommets_polygon:
            test = False
            # Liste des points d'intersections avec les segments du polygon
            liste_intersections = list()

            # Segment de référence du point O au sommet
            segment_sommet = segment_classe(self.O, sommet)

            # Pour chaque sommet : on parcours la liste de tous les segments
            # du polygon
            for segment in self.liste_segments_polygon:
                # On cherche les points d'intersection entre la demi droite
                # définie par O et le sommet et le segment considéré du polygon
                I = intersection_demi_droite_segment(segment_sommet, segment)

                # Si un point d'intersection existe
                if I is not None:
                    '''Fonction de détection des sommets à revoir ?'''
                    # Les sommets étant détectés deux fois,
                    # on ne les compte qu'une
                    if liste_intersections.count([dist(self.O, I), I,
                        self.liste_sommets_polygon.index(sommet)]) == 1:
                        continue
                    # On l'ajoute à la liste des intersections détectés.
                    liste_intersections.append([dist(self.O, I), I,
                        self.liste_sommets_polygon.index(sommet)])

            # Pour chaque sommet, une fois toutes les intersections trouvés,
            # on cherche la plus proche du point O
            liste_intersections.sort()
            min_intersection = liste_intersections[0]
            I = min_intersection[1]

            result = self.status_intersections(liste_intersections, sommet,
                                               list())
            for intersection in result:
                liste_intersections_def.append(intersection)

        # Dans le mode de démonstration, on affiche les intersections
        # définitives trouvés avec la couleur associée à son status.
        if self.mode_demo:
            for intersection in liste_intersections_def:
                I = intersection[0]
                # print(I)
                self.canvas.create_line(self.O.x, self.O.y, I.x,
                                        I.y, fill='red',
                                        tag='demo')
                if intersection[1] == 'AHEAD':
                    continue
                elif intersection[1] == 'EQUALS':
                    color = 'green'
                else:
                    color = 'blue'
                self.canvas.create_oval(I.x-size, I.y-size, I.x+size, I.y+size,
                                        fill=color, tag='demo')

        # Liste des intersections dans l'ordre
        liste_intersections_ordones = list()
        count = 0

        # Une fois toutes les intersections trouvés, il convient de les trier
        # pour en faire un polygon d'éclairage
        # On parcous la liste des segments du polygon dans l'ordre
        for segment in self.liste_segments_polygon:
            print(segment)
            intersections_sur_segment = list()
            # On parcous la liste des intersections trouvés plus haut
            for intersection in liste_intersections_def:
                if str(segment) == "[(315,63),(373,57)]":
                    print(intersection[0])
                I = intersection[0]
                # Si l'intersection est sur le segment considéré, on l'ajoute
                # dans une nouvelle liste.
                if point_appartient_segment(I, segment, intersection[1]):
                    if not intersection[1] == "AHEAD":
                        intersections_sur_segment.append(
                            [dist(segment.A, I), intersection])
                    # Les cas "AHEAD" sont ignorés et supprimés
                    else:
                        liste_intersections_def.remove(intersection)
            # Une fois la liste tous les points d'intersections se trouvant sur
            # le segment considéré sont trouvés
            # On vérifie qu'il y en a au moins un
            if not intersections_sur_segment:
                continue
            # On les tris dans l'ordre croissant de leur distance avec
            # le premier point du segment
            intersections_sur_segment.sort()
            # Une fois dans l'ordre
            for intersection in intersections_sur_segment:
                # On leur attribut leur numéro
                count += 1
                I = (intersection[1][0].x, intersection[1][0].y)
                # On sauvegarde les coordonnées de l'intersections dans une
                # nouvelle liste
                liste_intersections_ordones.append(I)
                liste_intersections_def.remove(intersection[1])
                # Dans le mode de démo, on affiche leur numéro à côté
                if self.mode_demo:
                    self.canvas.create_text(I[0], I[1]-10, text=count,
                                            tag='demo')
        # On retourne la liste ordonnée des intersections
        # correspondant au polygon d'éclairage
        '''print(liste_intersections_def)
        for I in liste_intersections_def:
            print(I[0])'''
        return liste_intersections_ordones

    def status_intersections(self, liste_intersections, sommet,
                             points_indentifies):
        '''DocString'''
        liste_intersections.sort()
        I = liste_intersections[0][1]
        indice_sommet = liste_intersections[0][2]

        recursif = False
        if points_indentifies:
            recursif = True

        est_sommet = False

        # Si il s'agit du sommet en cours
        if point_egaux(I, sommet):
            est_sommet = True

        # Si il s'agit d'un autre sommet du polygon
        elif self.sommet_du_polygon(I):
            est_sommet = True

        if est_sommet:
            # On ajoute le statut du point indentifié
            status = "EQUALS"
            if recursif:
                status = "BEYOND"
            points_indentifies.append([I, status])

            # Si il ne s'agit pas d'une projection, fin de traitement
            if not self.verif_si_projection(sommet, indice_sommet):
                return points_indentifies
            # Sinon, on passe à l'intersection suivante
            del liste_intersections[0]
            
            if not liste_intersections:
                return points_indentifies
            # On rappelle la fonction
            return self.status_intersections(liste_intersections, sommet,
                                             points_indentifies)

        status = "AHEAD"
        if recursif:
            status = "BEYOND"
        points_indentifies.append([I, status])
        return points_indentifies

    def verif_si_projection(self, sommet, indice_sommet):
        '''DocString'''
        det1 = determinant_3_points(self.O, sommet,
            self.liste_sommets_polygon[indice_sommet-1])

        if indice_sommet == len(self.liste_sommets_polygon)-1:
            indice_sommet = -1

        det2 = determinant_3_points(self.O, sommet,
            self.liste_sommets_polygon[indice_sommet+1])

        if signe(det1) == 0 or signe(det2) == 0:
            return False

        if signe(det1) == signe(det2):
            return True
        return False

    def sommet_du_polygon(self, I):
        '''DocString'''
        for sommet in self.liste_sommets_polygon:
            if point_egaux(I, sommet):
                return True
        return False

'''
def polygon_eclairage2(start_point, polygon, canvas, mode_demo=False):
    """Arguments :
        - start_point : Tuple ou liste sous la forme (x, y) ou [x, y]
        - polygon : Liste de sommets sous la forme  [(xA, yA), (xB, yB) ...]
        - canvas : Canvas de dessin
        - mode_demo : Boolean, True pour activer le mode de démonstration
    Retourne le polygon d'éclairage sous la forme d'une liste de points
    au format tuple : [(xA, yA), (xB, yB) ...]"""
    print("====================")
    # Vérifications élémentaires
    if not (type(start_point) == tuple or type(start_point) == list):
        return None
    if not (len(start_point) == 2):
        return None

    canvas.delete("demo")

    # Création d'une liste contenant les segments du polygon
    liste_segments_polygon = list()
    A = point_classe(polygon[0][0], polygon[0][1])
    for i in range(1, len(polygon)):
        B = point_classe(polygon[i][0], polygon[i][1])
        liste_segments_polygon.append(segment_classe(A, B))
        A = B
    B = point_classe(polygon[0][0], polygon[0][1])
    liste_segments_polygon.append(segment_classe(A, B))

    # Création d'une liste contenant les sommets du polygon
    liste_sommets_polygon = list()
    for point in polygon:
        liste_sommets_polygon.append(point_classe(point[0], point[1]))

    # Le point O est le point où l'on souhaite connaître le polygon d'éclairage
    O = point_classe(start_point[0], start_point[1])

    if mode_demo:
        # Affichage de la source lumineuse en jaune
        canvas.create_oval(O.x-size, O.y-size, O.x+size, O.y+size,
                           fill='white', tag='demo')

    # Liste qui contiendra les intersections retenues (la plus proche du point
    # et les projections) avec leur status
    liste_intersections_def = list()

    # Pour chaque sommet du polygon, on va chercher son projeté le plus proche
    for sommet in liste_sommets_polygon:
        # Liste des points d'intersections avec les segments du polygon
        liste_intersections = list()

        # Segment de référence du point O au sommet
        segment_sommet = segment_classe(O, sommet)

        # Pour chaque sommet : on parcours la liste de tous les segments
        # du polygon
        for segment in liste_segments_polygon:
            # On cherche les points d'intersection entre la demi droite
            # définie par O et le sommet et le segment considéré du polygon
            I = intersection_demi_droite_segment(segment_sommet, segment)
            # Dans le cas de points alignés
            if I == "Infinite":
                print("INFINITE")
                # Le point d'intersections est celui le plus proche de O
                liste = [[dist(O, segment.A), segment.A],
                         [dist(O, segment.B), segment.B]]
                I = min(liste)[1]
                minimum = min(liste)
                liste_intersections.append(minimum)
            # Si un point d'intersection existe
            if I is not None:
                Fonction de détection des sommets à revoir ?
                # Les sommets étant détectés deux fois, on ne les compte qu'une
                if liste_intersections.count([dist(O, I), I, liste_sommets_polygon.index(sommet)]) == 1:
                    continue
                # On l'ajoute à la liste des intersections détectés.
                liste_intersections.append([dist(O, I), I, liste_sommets_polygon.index(sommet)])

        # Pour chaque sommet, une fois toutes les intersections trouvés,
        # on cherche la plus proche du point O
        liste_intersections.sort()
        min_intersection = liste_intersections[0]
        I = min_intersection[1]

        # Un fois l'intersection la plus proche trouvée, il convient
        # d'identifier son status
        status_found = False
        status = None
        projection = False
        i = 0
        print(I)
  
        # On cherche le statut du point d'intersection trouvé
        while not status_found:
            i += 1
            projection = False
            for sommet2 in liste_sommets_polygon:
                if point_egaux(I, sommet2):
                    print("EQUALS")
                    status = "EQUALS"

                    if len(liste_intersections) == 1:
                        status_found = True

                    else:
                        indice_sommet = min_intersection[2]

                        det1 = determinant_3_points(O, sommet,
                            liste_sommets_polygon[indice_sommet-1])

                        if indice_sommet == len(liste_sommets_polygon)-1:
                            indice_sommet = -1

                        det2 = determinant_3_points(O, sommet,
                            liste_sommets_polygon[indice_sommet+1])
                        print(det1, det2)
                        if signe(det1) != signe(det2):
                            status_found = True
                            if i > 1:
                                status = "BEYOND"
                        else:
                            projection = True

                    liste_intersections_def.append([I, status])

            if not status_found:
                if not projection:
                    if i == 1:
                        status = "AHEAD"
                    else:
                        status = "BEYOND"
                    # On l'ajoute à la liste finale
                    liste_intersections_def.append([I, status])
                    status_found = True

                else:
                    # Il faut ensuite trouver sa projection
                    liste_intersections.remove(min_intersection)
                    # Il s'agit de l'intersection suivante la plus proche
                    min_intersection = liste_intersections[0]
                    I = min_intersection[1]
                    # On refait un tour de boucle pour déterminer le status
                    # de cette nouvelle intersection

    # Dans le mode de démonstration, on affiche les intersections définitives
    # trouvés avec la couleur associée à son status.
    if mode_demo:
        for intersection in liste_intersections_def:
            I = intersection[0]
            canvas.create_line(O.x, O.y, I.x, I.y,
                               fill='red', tag='demo')
            if intersection[1] == 'AHEAD':
                continue
            elif intersection[1] == 'EQUALS':
                color = 'green'
            else:
                color = 'blue'
            canvas.create_oval(I.x-size, I.y-size, I.x+size, I.y+size,
                               fill=color, tag='demo')

    # Liste des intersections dans l'ordre
    liste_intersections_ordones = list()
    count = 0

    # Une fois toutes les intersections trouvés, il convient de les trier
    # pour en faire un polygon d'éclairage

    # On parcous la liste des segments du polygon dans l'ordre
    for segment in liste_segments_polygon:
        intersections_sur_segment = list()
        # On parcous la liste des intersections trouvés plus haut
        for intersection in liste_intersections_def:
            I = intersection[0]
            # Si l'intersection est sur le segment considéré, on l'ajoute
            # dans une nouvelle liste.
            if point_appartient_segment(I, segment):
                if not intersection[1] == "AHEAD":
                    intersections_sur_segment.append(
                        [dist(segment.A, I), intersection])
                # Les cas "AHEAD" sont ignorés et supprimés
                else:
                    liste_intersections_def.remove(intersection)
        # Une fois la liste tous les points d'intersections se trouvant sur
        # le segment considéré sont trouvés
        # On vérifie qu'il y en a au moins un
        if not intersections_sur_segment:
            continue
        # On les tris dans l'ordre croissant de leur distance avec le premier
        # point du segment
        intersections_sur_segment.sort()
        # Une fois dans l'ordre
        for intersection in intersections_sur_segment:
            # On leur attribut leur numéro
            count += 1
            I = (intersection[1][0].x, intersection[1][0].y)
            # On sauvegarde les coordonnées de l'intersections dans une
            # nouvelle liste
            liste_intersections_ordones.append(I)
            liste_intersections_def.remove(intersection[1])
            # Dans le mode de démo, on affiche leur numéro à côté
            if mode_demo:
                canvas.create_text(I[0], I[1]-10, text=count, tag='demo')
    # On retourne la liste ordonnée des intersections
    # correspondant au polygon d'éclairage
    return liste_intersections_ordones'''
