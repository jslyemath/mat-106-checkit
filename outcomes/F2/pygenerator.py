import slye_math as sm
import random
import math
from fractions import Fraction


def generate(**kwargs):
    # We will only divide certain shapes certain ways in area models
    # 'shape' : [ways to divide]
    shapes_dict = {
        'circle': [2, 3, 4, 6, 8],
        'isosceles trapezoid': [2, 3, 6],
        'equilateral triangle': [2, 3],
        'regular hexagon': [2, 3, 4, 6],
        'rectangle': [2, 3, 4, 5, 6, 8],
        'semicircle': [2, 3, 4]
    }

    shapes_possibilities = [(shape, num) for shape, nums in shapes_dict.items() for num in nums]

    # def plot_area_model(shape='circle', numerator=1, denominator=1, dir_path='outcomes/F2/',
    #                     save_as='example_model.png'):
    #     filepath = os.path.join(dir_path, save_as)
    #
    #     def plot_circles(num, denom, filename='outcomes/F2/example_area_model.png'):
    #         n = math.ceil(num / denom)  # Number of circles to draw
    #         plt.figure(figsize=(10, 6))
    #         fig, ax = plt.subplots()
    #
    #         filled_wedges = 0  # Counter for the number of filled wedges
    #
    #         for i in range(n):
    #             x_offset = (2.1 * i)  # Horizontal offset for each circle
    #             r = 1  # Radius for each circle
    #             for j in range(denom):
    #                 theta1 = j * (360 / denom)  # Start angle of the sector
    #                 theta2 = (j + 1) * (360 / denom)  # End angle of the sector
    #
    #                 if filled_wedges < num:
    #                     facecolor = 'lightblue'
    #                     filled_wedges += 1
    #                 else:
    #                     facecolor = 'white'
    #
    #                 wedge = patches.Wedge((x_offset, 0), r, theta1, theta2, facecolor=facecolor, edgecolor='black')
    #                 ax.add_patch(wedge)
    #
    #         ax.set_aspect('equal')
    #         ax.set_xlim(-1, 2.1 * n - 1)
    #         ax.set_ylim(-1.1, 1.1)
    #         ax.axis('off')
    #
    #         # Save the plot to a file
    #         plt.savefig(filename, format='png', transparent=True, bbox_inches='tight')
    #         plt.cla()
    #         plt.clf()
    #         plt.close()
    #
    #         return None
    #
    #     def plot_trapezoids(num, denom, filename='outcomes/F2/example_area_model.png'):
    #         assert denom in [2, 3, 6], "denom must be 2, 3, or 6"
    #
    #         n = math.ceil(num / denom)  # Number of trapezoids to draw
    #         fig, ax = plt.subplots()
    #
    #         filled_shapes = 0  # Counter for the number of filled shapes
    #
    #         for i in range(n):
    #             x_offset = (2.1 * i)  # Horizontal offset for each trapezoid
    #             top_base = 1
    #             bottom_base = 2
    #             height = 1
    #
    #             # Base vertices of the trapezoid
    #             base_left = (x_offset - bottom_base / 2, 0)
    #             base_right = (x_offset + bottom_base / 2, 0)
    #             top_left = (x_offset - top_base / 2, height)
    #             top_right = (x_offset + top_base / 2, height)
    #             mid_base = (x_offset, 0)
    #             quarter_left = (x_offset - bottom_base / 4, 0)
    #             quarter_right = (x_offset + bottom_base / 4, 0)
    #             mid_top = (x_offset, height)
    #
    #             # Draw the base trapezoid
    #             trapezoid = patches.Polygon([base_left, base_right, top_right, top_left], closed=True,
    #                                         edgecolor='black', facecolor='none')
    #             ax.add_patch(trapezoid)
    #
    #             if denom == 2:
    #                 for j in range(2):
    #                     if filled_shapes < num:
    #                         facecolor = 'lightblue'
    #                         filled_shapes += 1
    #                     else:
    #                         facecolor = 'white'
    #
    #                     if j == 0:
    #                         shape = patches.Polygon([base_left, mid_base, mid_top, top_left], closed=True,
    #                                                 edgecolor='black', facecolor=facecolor)
    #                     else:
    #                         shape = patches.Polygon([mid_base, base_right, top_right, mid_top], closed=True,
    #                                                 edgecolor='black', facecolor=facecolor)
    #                     ax.add_patch(shape)
    #
    #             elif denom == 3:
    #                 for j in range(3):
    #                     if filled_shapes < num:
    #                         facecolor = 'lightblue'
    #                         filled_shapes += 1
    #                     else:
    #                         facecolor = 'white'
    #
    #                     if j == 0:
    #                         shape = patches.Polygon([base_left, mid_base, top_left], closed=True, edgecolor='black',
    #                                                 facecolor=facecolor)
    #                     elif j == 1:
    #                         shape = patches.Polygon([top_left, top_right, mid_base], closed=True, edgecolor='black',
    #                                                 facecolor=facecolor)
    #                     else:
    #                         shape = patches.Polygon([mid_base, base_right, top_right], closed=True, edgecolor='black',
    #                                                 facecolor=facecolor)
    #                     ax.add_patch(shape)
    #
    #             elif denom == 6:
    #                 vertices = [
    #                     (base_left, quarter_left, top_left),
    #                     (quarter_left, mid_base, top_left),
    #                     (mid_base, quarter_right, top_right),
    #                     (quarter_right, base_right, top_right),
    #                     (top_left, mid_top, mid_base),
    #                     (mid_base, mid_top, top_right)
    #                 ]
    #                 for j in range(6):
    #                     if filled_shapes < num:
    #                         facecolor = 'lightblue'
    #                         filled_shapes += 1
    #                     else:
    #                         facecolor = 'white'
    #
    #                     shape = patches.Polygon([vertices[j][0], vertices[j][1], vertices[j][2]], closed=True,
    #                                             edgecolor='black', facecolor=facecolor)
    #                     ax.add_patch(shape)
    #
    #         ax.set_aspect('equal')
    #         ax.set_xlim(-1, 2.1 * n - 1)
    #         ax.set_ylim(-0.1, 1.1)
    #         ax.axis('off')
    #
    #         # Save the plot to a file
    #         plt.savefig(filename, format='png', transparent=True, bbox_inches='tight')
    #         plt.cla()
    #         plt.clf()
    #         plt.close()
    #
    #         return None
    #
    #     def plot_triangles(num, denom, filename='outcomes/F2/example_area_model.png'):
    #         assert denom in [2, 3], "denom must be 2 or 3"
    #
    #         n = math.ceil(num / denom)  # Number of triangles to draw
    #         fig, ax = plt.subplots()
    #
    #         filled_shapes = 0  # Counter for the number of filled shapes
    #
    #         for i in range(n):
    #             x_offset = 1.1 * i  # Horizontal offset for each triangle
    #             side_length = 1
    #             height = math.sqrt(3) / 2 * side_length
    #
    #             # Base vertices of the triangle
    #             bottom_left = (x_offset - side_length / 2, 0)
    #             bottom_right = (x_offset + side_length / 2, 0)
    #             top = (x_offset, height)
    #             mid_base = (x_offset, 0)
    #             center = ((bottom_left[0] + bottom_right[0] + top[0]) / 3,
    #                       (bottom_left[1] + bottom_right[1] + top[1]) / 3)
    #
    #             # Draw the base triangle
    #             triangle = patches.Polygon([bottom_left, bottom_right, top], closed=True, edgecolor='black',
    #                                        facecolor='none')
    #             ax.add_patch(triangle)
    #
    #             if denom == 2:
    #                 for j in range(2):
    #                     if filled_shapes < num:
    #                         facecolor = 'lightblue'
    #                         filled_shapes += 1
    #                     else:
    #                         facecolor = 'white'
    #
    #                     if j == 0:
    #                         shape = patches.Polygon([bottom_left, mid_base, top], closed=True, edgecolor='black',
    #                                                 facecolor=facecolor)
    #                     else:
    #                         shape = patches.Polygon([mid_base, bottom_right, top], closed=True, edgecolor='black',
    #                                                 facecolor=facecolor)
    #                     ax.add_patch(shape)
    #
    #             elif denom == 3:
    #                 vertices = [
    #                     (bottom_left, center, top),
    #                     (bottom_right, center, top),
    #                     (bottom_left, bottom_right, center)
    #                 ]
    #                 for j in range(3):
    #                     if filled_shapes < num:
    #                         facecolor = 'lightblue'
    #                         filled_shapes += 1
    #                     else:
    #                         facecolor = 'white'
    #
    #                     shape = patches.Polygon([vertices[j][0], vertices[j][1], vertices[j][2]], closed=True,
    #                                             edgecolor='black', facecolor=facecolor)
    #                     ax.add_patch(shape)
    #
    #         ax.set_aspect('equal')
    #         ax.set_xlim(-0.5, 1.1 * n - 0.6)
    #         ax.set_ylim(-0.1, math.sqrt(3) / 2 + 0.1)
    #         ax.axis('off')
    #
    #         # Save the plot to a file
    #         plt.savefig(filename, format='png', transparent=True, bbox_inches='tight')
    #         plt.cla()
    #         plt.clf()
    #         plt.close()
    #
    #         return None
    #
    #     def plot_hexagons(num, denom, filename='outcomes/F2/example_area_model.png'):
    #         fig, ax = plt.subplots()
    #         filled_hexagons = 0
    #
    #         for i in range(math.ceil(num / denom)):
    #             x_offset = i * 2 * math.sqrt(3) / 2  # Adjust spacing based on hexagon dimensions
    #             y_offset = 0
    #
    #             # Generate vertices for a hexagon centered at (x_offset, y_offset)
    #             hexagon_vertices = [
    #                 (x_offset + math.cos(math.radians(60 * j)),
    #                  y_offset + math.sin(math.radians(60 * j)))
    #                 for j in range(6)
    #             ]
    #
    #             hexagon = patches.Polygon(hexagon_vertices, closed=True, edgecolor='black', facecolor='none')
    #             ax.add_patch(hexagon)
    #
    #             # Fill hexagon slices
    #             for j in range(denom):
    #                 facecolor = 'lightblue' if filled_hexagons < num else 'white'
    #                 filled_hexagons += 1 if filled_hexagons < num else 0
    #
    #                 # Calculate vertices for each slice within the hexagon
    #                 slice_vertices = [
    #                     (x_offset, y_offset),
    #                     hexagon_vertices[j],
    #                     hexagon_vertices[(j + 1) % 6]
    #                 ]
    #
    #                 slice_shape = patches.Polygon(slice_vertices, closed=True, edgecolor='black', facecolor=facecolor)
    #                 ax.add_patch(slice_shape)
    #
    #         ax.set_aspect('equal')
    #         ax.set_xlim(-1, 2 * math.sqrt(3) * math.ceil(num / denom))
    #         ax.set_ylim(-1.5, 1.5)
    #         ax.axis('off')
    #         plt.savefig(filename, format='png', transparent=True, bbox_inches='tight')
    #         plt.cla()
    #         plt.clf()
    #         plt.close()
    #         return None
    #
    #     def plot_rectangles(num, denom, filename='outcomes/F2/example_area_model.png'):
    #         n = math.ceil(num / denom)  # Number of main rectangles to draw
    #         fig, ax = plt.subplots()
    #
    #         filled_shapes = 0  # Counter for the number of filled shapes
    #
    #         for i in range(n):
    #             x_offset = 2.6 * i  # Horizontal offset for each main rectangle
    #             width = 2
    #             height = 1
    #             sub_rect_width = width / denom
    #
    #             # Draw the base rectangle
    #             base_rect = patches.Rectangle((x_offset, 0), width, height, edgecolor='black', facecolor='none')
    #             ax.add_patch(base_rect)
    #
    #             for j in range(denom):
    #                 if filled_shapes < num:
    #                     facecolor = 'lightblue'
    #                     filled_shapes += 1
    #                 else:
    #                     facecolor = 'white'
    #
    #                 # Calculate the position of the smaller rectangles
    #                 sub_rect = patches.Rectangle((x_offset + j * sub_rect_width, 0), sub_rect_width, height,
    #                                              edgecolor='black', facecolor=facecolor)
    #                 ax.add_patch(sub_rect)
    #
    #         ax.set_aspect('equal')
    #         ax.set_xlim(0, 2.6 * n - 0.6)
    #         ax.set_ylim(-0.1, 1.1)
    #         ax.axis('off')
    #
    #         # Save the plot to a file
    #         plt.savefig(filename, format='png', transparent=True, bbox_inches='tight')
    #         plt.cla()
    #         plt.clf()
    #         plt.close()
    #
    #         return None
    #
    #     def plot_semicircles(num, denom, filename='outcomes/F2/example_area_model.png'):
    #         n = math.ceil(num / denom)  # Number of semicircles to draw
    #         fig, ax = plt.subplots()
    #
    #         filled_shapes = 0  # Counter for the number of filled shapes
    #
    #         for i in range(n):
    #             x_offset = 2.5 * i  # Horizontal offset for each semicircle
    #             radius = 1
    #             theta_step = 180 / denom
    #
    #             for j in range(denom):
    #                 if filled_shapes < num:
    #                     facecolor = 'lightblue'
    #                     filled_shapes += 1
    #                 else:
    #                     facecolor = 'white'
    #
    #                 # Calculate the start and end angles for each sector
    #                 theta1 = j * theta_step
    #                 theta2 = (j + 1) * theta_step
    #
    #                 wedge = patches.Wedge((x_offset, 0), radius, theta1, theta2, edgecolor='black', facecolor=facecolor)
    #                 ax.add_patch(wedge)
    #
    #             # Draw the base semicircle outline
    #             arc = patches.Arc((x_offset, 0), 2 * radius, 2 * radius, angle=0, theta1=0, theta2=180,
    #                               edgecolor='black')
    #             ax.add_patch(arc)
    #
    #         ax.set_aspect('equal')
    #         ax.set_xlim(-1, 2.5 * n - 1.5)
    #         ax.set_ylim(-0.1, 1.1)
    #         ax.axis('off')
    #
    #         # Save the plot to a file
    #         plt.savefig(filename, format='png', transparent=True, bbox_inches='tight')
    #         plt.cla()
    #         plt.clf()
    #         plt.close()
    #
    #         return None
    #
    #     shapes_dict = {
    #         'circle': plot_circles,
    #         'isosceles trapezoid': plot_trapezoids,
    #         'equilateral triangle': plot_triangles,
    #         'regular hexagon': plot_hexagons,
    #         'rectangle': plot_rectangles,
    #         'semicircle': plot_semicircles
    #     }
    #
    #     shapes_dict[shape](numerator, denominator, filename=filepath)
    #
    # def plot_number_line(ticks, labels={0: '0'}, points=[], dir_path='outcomes/F2/', save_as='example_line.png'):
    #     filepath = os.path.join(dir_path, save_as)
    #
    #     line_thickness = 1.75
    #     tick_thickness = 1.75
    #     fig, ax = plt.subplots(figsize=(10, 2))
    #
    #     # Draw the double-sided arrow with specified line thickness
    #     arrow_style = '<|-|>'
    #     arrow = patches.FancyArrowPatch((-1.75, 0), (ticks + 0.75, 0),
    #                                     arrowstyle=arrow_style, linewidth=line_thickness, color='black',
    #                                     mutation_scale=30)
    #     ax.add_patch(arrow)
    #
    #     # Draw the ticks with specified thickness and label the first tick as 0
    #     for i in range(ticks):
    #         ax.plot([i, i], [0.07, -0.07], 'k-', linewidth=tick_thickness)
    #         if i in labels.keys():
    #             ax.annotate(f'{labels[i]}', xy=(i, 0), xytext=(i, -0.25), horizontalalignment='center', fontsize=14)
    #
    #     # Draw requested points
    #     for point in points:
    #         ax.scatter(point, 0, color='blue', s=70, zorder=5)
    #
    #     # Remove the axes
    #     ax.axis('off')
    #
    #     # Set the limits of the number line
    #     ax.set_xlim(-2, ticks + 1)
    #     ax.set_ylim(-0.5, 0.5)
    #
    #     # Save the figure to the specified file
    #     plt.savefig(filepath, bbox_inches='tight')
    #     plt.cla()
    #     plt.clf()
    #     plt.close()
    #
    # def create_null_graphic(dir_path='outcomes/F2/', save_as='null.png'):
    #     filepath = os.path.join(dir_path, save_as)
    #     source_file = 'assets/null.png'
    #
    #     # Copy the file to the new directory with the new name
    #     shutil.copy(source_file, filepath)
    #     return None
    #
    # def create_graphics_set(data, dir_path='assets/F2/'):
    #     # p1 graphics
    #     if data['p1_type'] == 'line':
    #         # prob
    #         p1_ticks = max(int(data['p1_orig_loc']), int(data['p1_requested_loc'])) + random.randint(1, 4)
    #         p1_labels = {0: '0', int(data['p1_orig_loc']): '1'}
    #         plot_number_line(p1_ticks, labels=p1_labels, dir_path=dir_path, save_as='p1_prob_model.png')
    #
    #         # ans
    #         p1_labels = {0: '0', int(data['p1_orig_loc']): '1',
    #                      int(data['p1_requested_loc']): f"{data['p1_requested_num']}/{data['p1_requested_denom']}"}
    #         points = [int(data['p1_requested_loc'])]
    #         plot_number_line(p1_ticks, labels=p1_labels, points=points, dir_path=dir_path, save_as='p1_ans_model.png')
    #     else:
    #         # prob
    #         create_null_graphic(dir_path=dir_path, save_as='p1_prob_model.png')
    #
    #         # ans
    #         p1_shape = data['p1_type']
    #         p1_numerator = int(data['p1_model_num'])
    #         p1_denominator = int(data['p1_model_denom'])
    #         plot_area_model(shape=p1_shape, numerator=p1_numerator, denominator=p1_denominator, dir_path=dir_path,
    #                         save_as='p1_ans_model.png')
    #
    #     # p2 graphics
    #     if data['p2_type'] == 'line':
    #         # prob
    #         p2_ticks = max(int(data['p2_orig_loc']), int(data['p2_requested_loc'])) + random.randint(1, 4)
    #         p2_labels = {0: '0', int(data['p2_orig_loc']): '1'}
    #         plot_number_line(p2_ticks, labels=p2_labels, dir_path=dir_path, save_as='p2_prob_model.png')
    #
    #         # ans
    #         p2_labels = {0: '0', int(data['p2_orig_loc']): '1',
    #                      int(data['p2_requested_loc']): f"{data['p2_requested_num']}/{data['p2_requested_denom']}"}
    #         points = [int(data['p2_requested_loc'])]
    #         plot_number_line(p2_ticks, labels=p2_labels, points=points, dir_path=dir_path, save_as='p2_ans_model.png')
    #     else:
    #         # prob
    #         create_null_graphic(dir_path=dir_path, save_as='p2_prob_model.png')
    #
    #         # ans
    #         p2_shape = data['p2_type']
    #         p2_numerator = int(data['p2_model_num'])
    #         p2_denominator = int(data['p2_model_denom'])
    #         plot_area_model(shape=p2_shape, numerator=p2_numerator, denominator=p2_denominator, dir_path=dir_path,
    #                         save_as='p2_ans_model.png')
    #
    #     # p3 graphics
    #     if data['p3_type'] == 'line':
    #         # prob
    #         p3_ticks = max(int(data['p3_orig_loc']), int(data['p3_requested_loc'])) + random.randint(1, 4)
    #         p3_labels = {0: '0', int(data['p3_orig_loc']): f"{data['p3_orig_num']}/{data['p3_orig_denom']}"}
    #         plot_number_line(p3_ticks, labels=p3_labels, dir_path=dir_path, save_as='p3_prob_model.png')
    #
    #         # ans
    #         p3_labels = {0: '0', int(data['p3_orig_loc']): f"{data['p3_orig_num']}/{data['p3_orig_denom']}",
    #                      int(data['p3_requested_loc']): f"{data['p3_requested_num']}/{data['p3_requested_denom']}"}
    #         points = [int(data['p3_requested_loc'])]
    #         plot_number_line(p3_ticks, labels=p3_labels, points=points, dir_path=dir_path, save_as='p3_ans_model.png')
    #     else:
    #         # prob
    #         create_null_graphic(dir_path=dir_path, save_as='p3_prob_model.png')
    #
    #         # ans
    #         p3_shape = data['p3_type']
    #         p3_numerator = int(data['p3_model_num'])
    #         p3_denominator = int(data['p3_model_denom'])
    #         plot_area_model(shape=p3_shape, numerator=p3_numerator, denominator=p3_denominator, dir_path=dir_path,
    #                         save_as='p3_ans_model.png')
    #
    #     return None
    #
    # generated_folder = 'assets/F2/generated/'
    #
    # with open('assets/F2/generated/seeds.json', 'r') as file:
    #     seeds_dict = json.load(file)
    #
    # print('Generating...')
    # # matplotlib has memory leaks that I can't figure out - do the ranges in batches
    # for i in range(0, 50):
    #     data = seeds_dict['seeds'][i]['data']
    #
    #     seed_folder = os.path.join(generated_folder, data['__seed__'])
    #     if not os.path.exists(seed_folder):
    #         os.makedirs(seed_folder)
    #
    #     create_graphics_set(data, dir_path=seed_folder)
    #     plt.cla()
    #     plt.clf()
    #     plt.close('all')
    #     if i % 10 == 0:
    #         print(f'{i}...')
    #
    # print('Done!')

    def gen_easy_line_prob():
        # Gives students a problem where the given is 1

        shape = 'line'
        # Choose from tick locations that have multiple divisors
        orig_loc = random.choice([6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28])
        orig_num = 1
        orig_denom = 1

        # Remove cases that are too easy for the requested denominator
        possible_requested_denoms = [x for x in sm.divisors(orig_loc) if x not in [1, 2, orig_loc]]
        requested_denom = random.choice(possible_requested_denoms)

        # Keep requested location within reasonable bounds
        possible_requested_nums = sm.rel_primes(requested_denom, stop=math.ceil(30 * requested_denom / orig_loc))
        requested_num = random.choice(possible_requested_nums)

        requested_loc = orig_loc * requested_num // requested_denom

        return shape, orig_loc, orig_num, orig_denom, requested_loc, requested_num, requested_denom

    def gen_hard_line_prob():
        # Gives students a problem where the given is not 1
        # Still easy enough that the denominator of the requested fraction can be obtained by subdivision of orig denom

        shape = 'line'
        # Choose from tick locations that have lots of divisors
        orig_loc = random.choice([12, 16, 18, 20, 24, 28, 30])

        # Given numerator must divide tick location, but avoid original tick location itself
        orig_loc_divisors = sm.divisors(orig_loc)
        orig_loc_divisors.remove(orig_loc)
        orig_num = random.choice(orig_loc_divisors)

        # Choose denominator that doesn't force us to simplify the fraction, and that prevents whole numbers
        potential_orig_denoms = sm.rel_primes(orig_num, stop=20)
        potential_orig_denoms.remove(1)
        orig_denom = random.choice(potential_orig_denoms)

        # To be able to subdivide, we need to carefully choose our requested denominator to share a divisor
        # Kick out 1 in certain cases to prevent edge cases
        remaining_divisors = sm.divisors(orig_loc / orig_num)
        if orig_num == 1:
            remaining_divisors.remove(1)
        k = random.choice(remaining_divisors)
        requested_denom = k * orig_denom
        potential_requested_nums = list(range(1, math.ceil(30 * orig_num * k / orig_loc)))

        # Prevent requested fraction from equaling given fraction
        if orig_num * requested_denom % orig_denom == 0:
            if orig_num * requested_denom // orig_denom in potential_requested_nums:
                potential_requested_nums.remove(orig_num * requested_denom // orig_denom)
        requested_num = random.choice(potential_requested_nums)

        # Calculate tick mark of requested fraction
        requested_loc = orig_loc // (orig_num * k) * requested_num

        # Simplifying the fraction for beauty and creating fun cases where requested denom ends up less than given denom
        requested_num, requested_denom = Fraction(requested_num, requested_denom).as_integer_ratio()

        return shape, orig_loc, orig_num, orig_denom, requested_loc, requested_num, requested_denom

    def gen_easy_area_prob():
        shape = random.choice(list(shapes_dict.keys()))
        model_denom = int(random.choice(shapes_dict[shape]))
        model_num = int(random.choice(sm.rel_primes(model_denom, stop=3 * model_denom)))
        orig_denom = int(1)
        orig_num = int(1)
        requested_num, requested_denom = model_num, model_denom

        return shape, model_num, model_denom, orig_num, orig_denom, requested_num, requested_denom

    def gen_hard_area_prob():
        shape_splits = shapes_possibilities[:]
        allow_prime_model_denom = random.choices([True, False], [0.2, 0.8], k=1)[0]
        if not allow_prime_model_denom:
            shape_splits = [x for x in shape_splits if x[1] not in (2,3,5,7,11)]
        shape, model_denom = random.choice(shape_splits)
        model_denom_factor_list = sm.divisors(model_denom)
        if model_denom not in (2,3,5,7,11):
            model_denom_factor_list = [x for x in model_denom_factor_list if x not in (1, model_denom)]
        orig_num = random.choice(model_denom_factor_list)
        denom_multiplier = model_denom // orig_num
        orig_denom_possibilities = sm.rel_primes(orig_num, start=2, stop = orig_num*3)
        orig_denom = random.choice(orig_denom_possibilities)
        requested_denom = denom_multiplier * orig_denom
        requested_num_possibilities = sm.rel_primes(requested_denom, stop=4*model_denom)
        if denom_multiplier == 1:
            requested_num_possibilities = [x for x in requested_num_possibilities if x != orig_num]
        requested_num = random.choice(requested_num_possibilities)
        model_num = requested_num

        return shape, model_num, model_denom, orig_num, orig_denom, requested_num, requested_denom

    hard_problem_type = random.choice(['number line', 'area model'])

    if hard_problem_type == 'number line':
        p1_type, p1_orig_loc, p1_orig_num, p1_orig_denom, p1_requested_loc, p1_requested_num, p1_requested_denom = gen_easy_line_prob()
        p1_text = f'Given the number line below, mark the value '
        p1_math = f'\\dfrac{{{p1_requested_num}}}{{{p1_requested_denom}}}'
        p1_prob_text = f'Number line with 1 labeled {p1_orig_loc} spaces to the right of 0'
        p1_ans_text = (f'A number line that is the same as the one given above, but with a blue point for '
                       f'{p1_requested_num}/{p1_requested_denom} labeled {p1_requested_loc} '
                       f'spaces to the right of 0.')
        p1_model_num = None
        p1_model_denom = None
        p1_ticks = max(p1_orig_loc, p1_requested_loc) + random.randint(1, 4)
        p1_label_b = '1'
        p1_label_c = p1_math

        p2_type, p2_model_num, p2_model_denom, p2_orig_num, p2_orig_denom, p2_requested_num, p2_requested_denom = gen_easy_area_prob()
        p2_text = f'If one {p2_type} represents 1, draw an area model for '
        p2_math = f'\\dfrac{{{p2_requested_num}}}{{{p2_requested_denom}}}'
        p2_prob_text = ''
        p2_ans_text = (f'A model of {p2_type}(s) each split equally into {p2_model_denom} parts. A total of '
                       f'{p2_model_num}  of these parts are shaded to represent {p2_requested_num}/{p2_requested_denom}.')
        p2_orig_loc = None
        p2_requested_loc = None
        p2_ticks = None
        p2_label_b = None
        p2_label_c = None

        p3_type, p3_orig_loc, p3_orig_num, p3_orig_denom, p3_requested_loc, p3_requested_num, p3_requested_denom = gen_hard_line_prob()
        p3_text_1 = f'Given the number line below, mark the value '
        p3_math_1 = ''
        p3_text_2 = ''
        p3_math_2 = f'\\dfrac{{{p3_requested_num}}}{{{p3_requested_denom}}}'
        p3_text_math = f'Given the number line below, mark the value $\\dfrac{{{p3_requested_num}}}{{{p3_requested_denom}}}$'
        p3_prob_text = f'Number line with {p3_orig_num}/{p3_orig_denom} labeled {p3_orig_loc} spaces to the right of 0'
        p3_ans_text = (f'A number line that is the same as the one given above, but with a blue point for '
                       f'{p3_requested_num}/{p3_requested_denom} labeled {p3_requested_loc} '
                       f'spaces to the right of 0.')
        p3_model_num = None
        p3_model_denom = None
        p3_ticks = max(p3_orig_loc, p3_requested_loc) + random.randint(1, 4)
        p3_label_b = f"\\dfrac{{{p3_orig_num}}}{{{p3_orig_denom}}}"
        p3_label_c = p3_math_2
    else:
        p1_type, p1_model_num, p1_model_denom, p1_orig_num, p1_orig_denom, p1_requested_num, p1_requested_denom = gen_easy_area_prob()
        p1_text = f'If one {p1_type} represents 1, draw an area model for '
        p1_math = f'\\dfrac{{{p1_requested_num}}}{{{p1_requested_denom}}}'
        p1_prob_text = ''
        p1_ans_text = (f'A model of {p1_type}(s) each split equally into {p1_model_denom} parts. A total of '
                       f'{p1_model_num}  of these parts are shaded to represent {p1_requested_num}/{p1_requested_denom}.')
        p1_orig_loc = None
        p1_requested_loc = None
        p1_ticks = None
        p1_label_b = None
        p1_label_c = None

        p2_type, p2_orig_loc, p2_orig_num, p2_orig_denom, p2_requested_loc, p2_requested_num, p2_requested_denom = gen_easy_line_prob()
        p2_text = f'Given the number line below, mark the value '
        p2_math = f'\\dfrac{{{p2_requested_num}}}{{{p2_requested_denom}}}'
        p2_prob_text = f'Number line with 1 labeled {p2_orig_loc} spaces to the right of 0'
        p2_ans_text = (f'A number line that is the same as the one given above, but with a blue point for '
                       f'{p2_requested_num}/{p2_requested_denom} labeled {p2_requested_loc} '
                       f'spaces to the right of 0.')
        p2_model_num = None
        p2_model_denom = None
        p2_ticks = max(p2_orig_loc, p2_requested_loc) + random.randint(1, 4)
        p2_label_b = '1'
        p2_label_c = p2_math

        p3_type, p3_model_num, p3_model_denom, p3_orig_num, p3_orig_denom, p3_requested_num, p3_requested_denom = gen_hard_area_prob()
        p3_text_1 = f'If one {p3_type} represents '
        p3_math_1 = f'\\dfrac{{{p3_orig_num}}}{{{p3_orig_denom}}}'
        p3_text_2 = ', draw an area model for '
        p3_math_2 = f'\\dfrac{{{p3_requested_num}}}{{{p3_requested_denom}}}'
        p3_text_math = (f'If one {p3_type} represents $\\dfrac{{{p3_orig_num}}}{{{p3_orig_denom}}}$, draw an area '
                        f'model for $\\dfrac{{{p3_requested_num}}}{{{p3_requested_denom}}}$')
        p3_prob_text = ''
        p3_ans_text = (f'A model of {p3_type}(s) each split equally into {p3_model_denom} parts. A total of '
                       f'{p3_model_num} of these parts are shaded. This makes it appear to be an area model for '
                       f'{p3_model_num}/{p3_model_denom}, but given that one {p3_type} represents {p3_orig_num}/{p3_orig_denom}, '
                       f'it actually represents {p3_requested_num}/{p3_requested_denom}.')
        p3_orig_loc = None
        p3_requested_loc = None
        p3_ticks = None
        p3_label_b = None
        p3_label_c = None

#TODO: Bring area_model_tikz.py into the main script for latex generation, align textemplate to this.
#TODO: Generate standalone tikz pictures locally based on seeds.

    return {
        'p1_type': p1_type,
        'p1_orig_loc': p1_orig_loc,
        'p1_orig_num': p1_orig_num,
        'p1_orig_denom': p1_orig_denom,
        'p1_requested_loc': p1_requested_loc,
        'p1_requested_num': p1_requested_num,
        'p1_requested_denom': p1_requested_denom,
        'p1_model_num': p1_model_num,
        'p1_model_denom': p1_model_denom,
        'p1_text': p1_text,
        'p1_math': p1_math,
        'p1_prob_text': p1_prob_text,
        'p1_ans_text': p1_ans_text,
        'p1_ticks': p1_ticks,
        'p1_label_b': p1_label_b,
        'p1_label_c': p1_label_c,

        'p2_type': p2_type,
        'p2_orig_loc': p2_orig_loc,
        'p2_orig_num': p2_orig_num,
        'p2_orig_denom': p2_orig_denom,
        'p2_requested_loc': p2_requested_loc,
        'p2_requested_num': p2_requested_num,
        'p2_requested_denom': p2_requested_denom,
        'p2_model_num': p2_model_num,
        'p2_model_denom': p2_model_denom,
        'p2_text': p2_text,
        'p2_math': p2_math,
        'p2_prob_text': p2_prob_text,
        'p2_ans_text': p2_ans_text,
        'p2_ticks': p2_ticks,
        'p2_label_b': p2_label_b,
        'p2_label_c': p2_label_c,

        'p3_type': p3_type,
        'p3_orig_loc': p3_orig_loc,
        'p3_orig_num': p3_orig_num,
        'p3_orig_denom': p3_orig_denom,
        'p3_requested_loc': p3_requested_loc,
        'p3_requested_num': p3_requested_num,
        'p3_requested_denom': p3_requested_denom,
        'p3_model_num': p3_model_num,
        'p3_model_denom': p3_model_denom,
        'p3_text_1': p3_text_1,
        'p3_math_1': p3_math_1,
        'p3_text_2': p3_text_2,
        'p3_math_2': p3_math_2,
        'p3_text_math': p3_text_math,
        'p3_prob_text': p3_prob_text,
        'p3_ans_text': p3_ans_text,
        'p3_ticks': p3_ticks,
        'p3_label_b': p3_label_b,
        'p3_label_c': p3_label_c,
    }