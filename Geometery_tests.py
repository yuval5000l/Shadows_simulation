from geometry_stuff import *

z1 = (0,0)
z2 = (10,10)
r = (0, 10)
r2 = (10, 0)
#print(round(math.cos((math.pi)/4)), round(math.sin((math.pi)/4)))
#print(angle_calculator_radians(r, (10,10)))
print(angle_calculator_radians(r, (6.339677891654465, 6.339677891654466)))
print(math.pi/6)
assert ray_segment_intersection(r, [z1, z2], math.pi) is None
assert ray_segment_intersection(r, [z1,z2], 0) == (10.0, 10.0)
assert ray_segment_intersection(r, [z1,z2], math.pi/2) == (0.0, 0.0)
assert ray_segment_intersection(r, [z1,z2], math.pi/4) == (5.0, 5.0)


assert ray_segment_intersection(r2, [z1, z2], 0) is None
assert ray_segment_intersection(r2, [z1,z2], (math.pi)/2) is None
assert (ray_segment_intersection(r2, [z1,z2], (math.pi))) == (0.0, 0.0)
assert (ray_segment_intersection(r2, (z1,z2), (5*math.pi)/4)) ==(5.0, 5.0)
assert (ray_segment_intersection(r2, [z1,z2],(3*math.pi)/2)) == (10.0, 10.0)


print(ray_segment_intersection(r, [z1,z2], math.pi/6))