from shapely.geometry import Point

# TODO Shall we call it OutPoint like OurUrl?
class PointEncoder():

    @staticmethod
    def point_to_coordinates_tuple(obj: Point) -> tuple:
        return (obj.x, obj.y)
    
    @staticmethod
    def point_to_coordinates_str(obj: Point) -> str:
            return f'({obj.x}, {obj.y})'
    
    @staticmethod
    def str_coordinates_to_point(data) -> Point:
        try:
            coordinates = eval(data)
            if isinstance(coordinates, tuple) and len(coordinates) == 2:
                return Point(coordinates[0], coordinates[1])
            else:
                raise ValueError("Invalid coordinates format in the input string.")
        except Exception as e:
            raise ValueError(f"Failed to parse the input string: {e}")