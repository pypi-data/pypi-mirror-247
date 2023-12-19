from collections import namedtuple
from typing import List
import statistics
import inspect
import dnaplotlib as dpl
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Wedge, Polygon
from matplotlib.lines import Line2D
from matplotlib.patheffects import Stroke
from .export import CryptResults, CDS_COLOR, RBS_COLOR, TERMINATOR_COLOR, PROMOTER_COLOR

def plot_dnaplotlib(results: CryptResults, output_path: str, plot_params=None):
    if not plot_params:
        plot_params = {}
    # Make the CDS designs for each frame
    cds_designs = {'annotations': {},
                    'framef0': {},
                    'framef1': {},
                    'framef2': {},
                    'framer0': {},
                    'framer1': {},
                    'framer2': {}}
    
    # Add the annotations
    # namedtuple('feature', ['name', 'strand', 'start', 'end', 'color', 'nest_level'])
    for feature in results.annotations:
        cds_designs['annotations'][feature.name] = {"name": feature.name,
                                                   "start": feature.start,
                                                   "end": feature.end,
                                                   "type": "CDS",
                                                   "strand": feature.strand,
                                                   "opts": {"color": feature.color,
                                                            "zorder_add": 100,
                                                            "label": feature.name,
                                                            "absolute_pos": [feature.start, feature.end],
                                                            'y_offset': 10+feature.nest_level*10
                                                            },
                                                   "metadata": {},
                                                   'renderer': custom_annotation
                                                   }


    results.translation_sites.sort(key=lambda x: x.start)

    smallest_expression = None
    largest_expression = None

    for i, site in enumerate(results.translation_sites):
        # Get the frame
        strand = site.strand
        if strand == "+":
            frame = site.start % 3
        elif strand == "-":
            frame = (len(results.sequence) - site.end) % 3
        else:
            raise ValueError("Strand must be + or -")
        

        # Assign the part to a frame

        part_design = {"name": i,
                       "start": site.start,
                       "end": site.end,
                       "type": "CDS",
                       "strand": "fwd",
                       "opts": {"color": CDS_COLOR},
                       "metadata": {}}

        frame_tgt = None
        if strand == "+" and frame == 0:
            frame_tgt = "framef0"
        elif strand == "+" and frame == 1:
            frame_tgt = "framef1"
        elif strand == "+" and frame == 2:
            frame_tgt = "framef2"
        elif strand == "-" and frame == 0:
            frame_tgt = "framer0"
        elif strand == "-" and frame == 1:
            frame_tgt = "framer1"
        elif strand == "-" and frame == 2:
            frame_tgt = "framer2"
        assert frame_tgt
        
        # Check whether or not this part nests with one already in frame
        duplicate = False
        for j, part in enumerate(cds_designs[frame_tgt].values()):
            compared_starts = [int(part["start"]), int(site.start)]
            compared_ends = [int(part["end"]), int(site.end)]
            if strand == "-":
                compared_starts = [int(part["end"]), int(site.end)]
                compared_ends = [int(part["start"]), int(site.start)]

            if compared_starts[0] <= compared_starts[1] and compared_ends[0] >= compared_ends[1]:
                if frame_tgt == "framer2":
                    print(f'Nested CDS from {site.start} to {site.end}')
                # completely nested
                # Set parts to be an RBS
                part_design['type'] = "RBS"
                part_design['opts']['color'] = RBS_COLOR
                part_design['opts']['zorder_add'] = 50
                part_design['renderer'] = custom_rbs
                part_design['opts']['absolute_pos'] = [site.start-5, site.start+5]
                part_design['metadata']['strength'] = site.expression # (Can do expression or burden here)

                if smallest_expression is None or part_design['metadata']['strength'] < smallest_expression:
                    smallest_expression = part_design['metadata']['strength']
                if largest_expression is None or part_design['metadata']['strength'] > largest_expression:
                    largest_expression = part_design['metadata']['strength']


                break
            elif compared_starts[0] >= compared_starts[1] and compared_ends[0] <= compared_ends[1]:
                # Contains the other part
                if part['type'] == "RBS":
                    continue # Already contained by something else
                if frame_tgt == "framer2":
                    print(f'Completely containing CDS from {site.start} to {site.end}')
                # Set parts to be a CDS
                part_design['renderer'] = custom_cds
                part_design['opts']['absolute_pos'] = [site.start, site.end]
                part_design['metadata']['strength'] = site.expression
                # Change contained part to be an RBS
                part['type'] = "RBS"
                part['opts']['color'] = RBS_COLOR
                part['opts']['zorder_add'] = 50
                part['renderer'] = custom_rbs
                nested_start = part['opts']['absolute_pos'][0]
                part['opts']['absolute_pos'] = [nested_start-5, nested_start+5]

                if smallest_expression is None or part_design['metadata']['strength'] < smallest_expression:
                    smallest_expression = part_design['metadata']['strength']
                if largest_expression is None or part_design['metadata']['strength'] > largest_expression:
                    largest_expression = part_design['metadata']['strength']
                break
        else:
            # Set the part to be a CDS
            if frame_tgt == "framer2":
                print(f"Non-nested CDS from {site.start} to {site.end}")
            part_design['renderer'] = custom_cds
            part_design['opts']['absolute_pos'] = [site.start, site.end]
            part_design['metadata']['strength'] = site.expression

            if smallest_expression is None or part_design['metadata']['strength'] < smallest_expression:
                smallest_expression = part_design['metadata']['strength']
            if largest_expression is None or part_design['metadata']['strength'] > largest_expression:
                largest_expression = part_design['metadata']['strength']
        
        if not duplicate:
            cds_designs[frame_tgt][i] = part_design

    cds_designs = {k: list(v.values()) for k, v in cds_designs.items()}

    # Add RBS's at the beginning of each CDS
    for frame, parts in cds_designs.items():
        if frame == "annotations":
            continue
        for i, part in enumerate(parts):
            if part['type'] == "CDS":
                # Add an RBS
                rbs_design = {"name": i,
                            "start": part['start'],
                            "end": part['start'],
                            "type": "RBS",
                            "strand": "fwd",
                            "opts": {"color": RBS_COLOR},
                            "renderer": custom_rbs,
                            "metadata": {}}
                rbs_design['opts']['absolute_pos'] = [part['start']-5, part['start']+5]
                rbs_design['opts']['zorder_add'] = 50
                rbs_design['metadata']['strength'] = part['metadata']['strength']
                cds_designs[frame].append(rbs_design)



    # Check to make sure feature labels are not overlapping
    highest_label = 0
    moved_something = True
    while moved_something:
        moved_something = False
        for frame, parts in cds_designs.items():
            if frame != "annotations":
                continue
            for i, part in enumerate(parts):
                if not part['opts'].get('label', False) or not part['opts'].get('y_offset', False):
                    continue
                for j, part2 in enumerate(parts):
                    if not part2['opts'].get('label', False) or not part2['opts'].get('y_offset', False):
                        continue
                    if i == j:
                        continue
                    # Move parts if they are overlapping and have the same y_offset  # TODO: check for annotations within each other rather than proximity to centers
                    if abs(statistics.mean(part['opts']['absolute_pos']) - statistics.mean(part2['opts']['absolute_pos'])) < 100 or \
                        abs(statistics.mean(part['opts']['absolute_pos']) - statistics.mean(part2['opts']['absolute_pos'])) == 0:
                        # Move the label up
                        if part['opts'].get('y_offset', False) and \
                            part2['opts'].get('y_offset', False) and \
                            part['opts']['y_offset'] == part2['opts']['y_offset']:
                            moved_something = True
                            part2['opts']['y_offset'] += 10
                            if part2['opts']['y_offset'] > highest_label:
                                highest_label = part2['opts']['y_offset']

    print(f'Expression range: {smallest_expression} to {largest_expression}')

    # Adjust the size of the RBSs to represent their strength
    for frame, parts in cds_designs.items():
        for i, part in enumerate(parts):
            if part['type'] == "RBS":
                # Adjust the size of the RBS
                strength = part['metadata']['strength']
                percent_max = strength / largest_expression
                part['opts']['x_extent'] = 20*percent_max


    '''
    # Make a new cds_design for promoters and terminators
    cds_designs['rna'] = {}
    for i, site in enumerate(results.promoters):
        cds_designs['rna'][i] = {"name": i,
                            "start": site.TSSpos,
                            "end": site.TSSpos+10,
                            "type": "Promoter",
                            "strand": "fwd",
                            "opts": {"color": PROMOTER_COLOR},
                            "renderer": custom_promoter,
                            "metadata": {}}
        cds_designs['rna'][i]['opts']['absolute_pos'] = [site.TSSpos, site.TSSpos+10]
        cds_designs['rna'][i]['opts']['label'] = f"Promoter: {str([site.TSSpos, site.TSSpos+10])}"
        cds_designs['rna'][i]['opts']['label_y_offset'] = -25
    '''

    backbones = [False]*len(cds_designs)
    backbones[0] = True
    plot_params['backbones'] = backbones
    
    plot_dna(cds_designs, output_path+"_plot.svg", plot_params, None, results.sequence)


def plot_dna(dna_designs, out_filename, plot_params, regs_info, sequence, circular=False, hpad=0):
    # Create the renderer
    left_pad = 0.0
    right_pad = 0.0
    scale = 1.0
    linewidth = 1.0
    fig_y = 500.0
    fig_x = 5.0
    if plot_params:
        if 'backbone_pad_left' in list(plot_params.keys()):
            left_pad = plot_params['backbone_pad_left']
        if 'backbone_pad_right' in list(plot_params.keys()):
            right_pad = plot_params['backbone_pad_right']
        if 'scale' in list(plot_params.keys()):
            scale = plot_params['scale']
        if 'linewidth' in list(plot_params.keys()):
            linewidth = plot_params['linewidth']
        if 'fig_y' in list(plot_params.keys()):
            fig_y = plot_params['fig_y']
        if 'fig_x' in list(plot_params.keys()):
            fig_x = plot_params['fig_x']
        if 'axis_y' not in list(plot_params.keys()):
            plot_params['axis_y'] = 35
        plot_params.get('full_backbone', 'False')
        backbones = plot_params.get('backbones', None)
    else:
        plot_params = {}
        plot_params['axis_y'] = 35

    if backbones and len(backbones) != len(dna_designs):
        raise ValueError("The number of backbones must match the number of designs")

    dr = DNARenderer(scale=scale, linewidth=linewidth,
                            backbone_pad_left=left_pad, 
                            backbone_pad_right=right_pad,
                            full_backbone=plot_params['full_backbone'])

    # We default to the standard regulation renderers
    reg_renderers = dr.std_reg_renderers()
    # We default to the SBOL part renderers
    part_renderers = dr.SBOL_part_renderers()

    # Create the figure
    fig = plt.figure(figsize=(fig_x,fig_y))

    # Cycle through the designs an plot on individual axes
    design_list = sorted(dna_designs.keys())
    if(regs_info != None):
        regs_list   = sorted(regs_info.keys())

    num_of_designs = len(design_list)
    ax_list = []
    max_dna_len = 0.0
    for i in range(num_of_designs):
        # Create axis for the design and plot
        regs = None
        if(regs_info != None):
            regs   =  regs_info[i]
        design =  dna_designs[design_list[i]]  # List of features on a given strand

        ax = fig.add_subplot(num_of_designs,1,i+1)
        if 'show_title' in list(plot_params.keys()) and plot_params['show_title'] == 'Y':
            ax.set_title(design_list[i], fontsize=8)
        start, end = dr.renderDNA(ax, design, part_renderers, regs, reg_renderers)

        dna_len = end-start
        if max_dna_len < dna_len:
            max_dna_len = dna_len
        ax_list.append(ax)
    if plot_params["full_backbone"]:
        max_dna_len = len(sequence)*1.01+right_pad
    for i, ax in enumerate(ax_list):
        ax.set_xticks([])
        ax.set_yticks([])
        # Set bounds
        ax.set_xlim([-left_pad,
                    max_dna_len+(0.01*max_dna_len)+right_pad])
        ax.set_ylim([-plot_params['axis_y'],plot_params['axis_y']])
        if plot_params['full_backbone']:
            ax.set_xlim([-left_pad, len(sequence)*1.01+right_pad])
            ax.set_ylim([-plot_params['axis_y'],plot_params['axis_y']])
            dr.plot_backbone(ax, -left_pad, len(sequence)*1.01+right_pad, circular=circular)
        elif backbones[i]:
            ax.set_xlim([-left_pad, len(sequence)*1.01+right_pad])
            ax.set_ylim([-plot_params['axis_y'],plot_params['axis_y']])
            dr.plot_backbone(ax, -left_pad, len(sequence)*1.01+right_pad, circular=circular)

        ax.set_aspect('equal')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

    # Update the size of the figure to fit the constructs drawn
    fig_x_dim = max_dna_len/70.0
    if fig_x_dim < 1.0:
        fig_x_dim = 1.0
    fig_y_dim = (0.8)*len(ax_list)
    fig.tight_layout(h_pad=hpad)
    plt.gcf().set_size_inches( (fig_x_dim, fig_y_dim) )

    # Save the figure
    fig.savefig(out_filename, transparent=False, dpi=300)
    # Clear the plotting cache
    plt.close('all')

class DNARenderer(dpl.DNARenderer):
    def __init__(self, **kwargs):
        super_arguments = inspect.getargspec(super().__init__).args
        accepted_arguments = super_arguments + ["full_backbone"]
        super().__init__(**{k: v for k, v in kwargs.items() if k in super_arguments})
        if "full_backbone" in kwargs.keys():
            self.full_backbone = kwargs["full_backbone"]
        for key in kwargs.keys():
            if key not in accepted_arguments:
                raise ValueError("Unrecognized argument: {}".format(key))
    
    def renderDNA(self, ax, parts, part_renderers, regs=None, reg_renderers=None, plot_backbone=False, circular=False):
        """ Render the parts on the DNA and regulation.
        Parameters
        ----------
        ax : matplotlib.axes
            Axes to draw the design to.
        parts : list(dict)
            The design to draw. This is a list of dicts, where each dict relates to
            a part and must contain the following keys:
            - name (string)
            - type (string)  
            - fwd (bool)
            - start (float, optional)
            - end (float, optional)
            These will then be drawn in accordance with the renders selected
        part_renderers : dict(functions)
            Dict of functions where the key in the part type and the dictionary returns
            the function to be used to draw that part type.
        regs : list(dict) (default=None)
            Regulation present in the design. This is a list of dicts, where each dict
            relates to a single regulation arc and must contain the following keys:
            - type (string)
            - from_part (part object dict)  
            - to_part (part object dict)
            These will then be drawn in accordance with the renders selected.
        reg_renderers : dict(functions) (default=None)
            Dict of functions where the key in the regulation type and the dictionary 
            returns the function to be used to draw that regulation type.
        Returns
        -------
        start : float
            The x-point in the axis space that drawing begins.
        end : float
            The x-point in the axis space that drawing ends.
        """
        # Update the matplotlib rendering default for drawing the parts (we want mitered edges)
        mpl.rcParams['lines.dash_joinstyle']  = 'miter'
        mpl.rcParams['lines.dash_capstyle']   = 'butt'
        mpl.rcParams['lines.solid_joinstyle'] = 'miter'
        mpl.rcParams['lines.solid_capstyle']  = 'projecting'
        # Make text editable in Adobe Illustrator
        mpl.rcParams['pdf.fonttype']          = 42 
        # Plot the parts to the axis
        part_num = 0
        prev_end = 0
        first_start = 0
        first_part = True

        for part in parts:
            keys = list(part.keys())

            # Check the part has minimal details required
            if 'type' in keys:
                if 'fwd' not in keys:
                    part['fwd'] = True
                elif part['fwd'] is False and 'start' in keys and 'end' in keys:
                    start = part['start']
                    end = part['end']
                    part['end'] = start
                    part['start'] = end
                
                if 'start' not in keys:
                    if part['fwd'] == True:
                        part['start'] = part_num
                    else:
                        part['start'] = part_num+1
                if 'end' not in keys:
                    if part['fwd'] == True:
                        part['end'] = part_num+1
                    else:
                        part['end'] = part_num
                
                # Extract custom part options (if available)
                part_opts = None
                if 'opts' in list(part.keys()):
                    part_opts = part['opts']
                # Use the correct renderer
                if 'renderer' in list(part.keys()):
                    # Use custom renderer
                    prev_start, prev_end = part['renderer'](ax, part['type'], part_num, 
                                     part['start'], part['end'], prev_end,
                                     self.scale, self.linewidth, 
                                     opts=part_opts)

                    #update start,end for regulation
                    #part['start'] = prev_start
                    #part['end'] = prev_end

                    if first_part == True:
                        first_start = prev_start
                        first_part = False
                else:
                    # Use standard renderer, if one exists
                    if part['type'] in list(part_renderers.keys()):
                        prev_start, prev_end = part_renderers[part['type']](ax, 
                                       part['type'], part_num, 
                                       part['start'], part['end'], 
                                       prev_end, self.scale, 
                                       self.linewidth, opts=part_opts)
                        
                        #update start,end for regulation [TEG]
                        if part['fwd'] == True:
                            part['start'] = prev_start
                            part['end'] = prev_end
                        else:
                            part['start'] = prev_end
                            part['end'] = prev_start
                        
                        if first_part == True:
                            first_start = prev_start
                            first_part = False
            part_num += 1

        # Plot the backbone (z=1)
        if plot_backbone == True:
            if not self.full_backbone:
                backbone_start = first_start-self.backbone_pad_left
                backbone_end = prev_end+self.backbone_pad_right
                self.plot_backbone(ax, backbone_start, backbone_end, circular=circular)
        return first_start, prev_end

    def plot_backbone(self, ax, backbone_start, backbone_end, circular=False):
        kwargs = dict(linewidth=self.linewidth, color=self.linecolor, zorder=10)
        if circular == False:
            l1 = Line2D([backbone_start,backbone_end], [0,0], **kwargs)
            ax.add_line(l1)
        else:
            rad = 5
            if self.circular_depth < 2*rad:
                self.circular_depth = 2*rad
            verts = [
                (backbone_start, 0),                                # moveto
                (backbone_start - rad, 0),                          # curve3 control
                (backbone_start - rad, -rad),                       # curve3 end
                (backbone_start - rad, -self.circular_depth + rad), # lineto
                (backbone_start - rad, -self.circular_depth),       # curve3 control
                (backbone_start, -self.circular_depth),             # curve3 end
                (backbone_end, -self.circular_depth),               # lineto
                (backbone_end + rad, -self.circular_depth),         # curve3 control
                (backbone_end + rad, -self.circular_depth + rad),   # curve3 end
                (backbone_end + rad, -rad),                         # lineto
                (backbone_end + rad, 0),                            # curve3 control
                (backbone_end, 0),                                  # curve3 end
                (backbone_start, 0),                                # lineto
            ]
            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO,
                        Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3,
                        Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3,
                        Path.LINETO]
            path = Path(verts, codes)
            patch = PathPatch(path, fill=False, **kwargs)
            ax.add_patch(patch)
        pass

def custom_rbs(ax, type, num, start, end, prev_end, scale, linewidth, opts):
    """ Built-in SBOL ribosome binding site renderer.
    """
    # Default options
    zorder_add = 0.0
    color = (0.7,0.7,0.7)
    start_pad = 2.0
    end_pad = 2.0
    x_extent = 10.0
    edgecolor = (0,0,0)
    # Reset defaults if provided
    if opts == None:
        opts = {}
    zorder_add = opts.get('zorder_add', zorder_add)
    color = opts.get('color', color)
    start_pad = opts.get('start_pad', start_pad)
    end_pad = opts.get('end_pad', end_pad)
    x_extent = opts.get('x_extent', x_extent)
    linewidth = opts.get('linewidth', linewidth)
    edgecolor = opts.get('edge_color', edgecolor)
    absolute_pos = opts.get('absolute_pos', None)

    # Draw the RBS

    # Sanity Checking
    if not absolute_pos:
        raise ValueError("RBS must be drawn with absolute_pos option set.")
    if not isinstance(absolute_pos, list):
        raise ValueError("RBS must be drawn with absolute_pos option set to a list.")
    if not len(absolute_pos) == 2:
        raise ValueError("RBS must be drawn with absolute_pos option set to a list of length 2.")
    if not isinstance(absolute_pos[0], int) or not isinstance(absolute_pos[1], int):
        raise ValueError("RBS must be drawn with absolute_pos option set to a list of integers.")


    start = absolute_pos[0]
    end = absolute_pos[1]



    if start > end:
        rbs_center = ((start+end)/2.0,0)
        w1 = Wedge(rbs_center, x_extent/2.0, 180, 360, linewidth=linewidth, 
                   facecolor=color, edgecolor=edgecolor, zorder=8+zorder_add)
        ax.add_patch(w1)
    else:
        rbs_center = ((start+end)/2.0,0)
        w1 = Wedge(rbs_center, x_extent/2.0, 0, 180, linewidth=linewidth, 
                   facecolor=color, edgecolor=edgecolor, zorder=8+zorder_add)
        ax.add_patch(w1)

    if opts != None and 'label' in list(opts.keys()):
        dpl.write_label(ax, opts['label'], rbs_center[0], opts=opts)

    return prev_end, prev_end


def custom_cds(ax, type, num, start, end, prev_end, scale, linewidth, opts):
    """ Built-in SBOL coding sequence renderer."""
    # Default options
    zorder_add = 0.0
    color = (0.7,0.7,0.7)
    hatch = ''
    start_pad = 1.0
    end_pad = 1.0
    y_extent = 2
    x_extent = 30
    arrowhead_height = 4
    arrowhead_length = 8
    edgecolor = (0,0,0)
    # Reset defaults if provided
    if opts != None:
        if 'zorder_add' in list(opts.keys()):
            zorder_add = opts['zorder_add']
        if 'color' in list(opts.keys()):
            color = opts['color']
        if 'hatch' in list(opts.keys()):
            hatch = opts['hatch']
        if 'start_pad' in list(opts.keys()):
            start_pad = opts['start_pad']
        if 'end_pad' in list(opts.keys()):
            end_pad = opts['end_pad']
        if 'y_extent' in list(opts.keys()):
            y_extent = opts['y_extent']
        if 'x_extent' in list(opts.keys()):
            x_extent = opts['x_extent']
        if 'arrowhead_height' in list(opts.keys()):
            arrowhead_height = opts['arrowhead_height']
        if 'arrowhead_length' in list(opts.keys()):
            arrowhead_length = opts['arrowhead_length']
        if 'linewidth' in list(opts.keys()):
            linewidth = opts['linewidth']
        if 'scale' in list(opts.keys()):
            scale = opts['scale']
        if 'edge_color' in list(opts.keys()):
            edgecolor = opts['edge_color']
    
    absolute_pos = opts.get('absolute_pos', None)

    # Sanity Checking
    if not absolute_pos:
        raise ValueError("RBS must be drawn with absolute_pos option set.")
    if not isinstance(absolute_pos, list):
        raise ValueError("RBS must be drawn with absolute_pos option set to a list.")
    if not len(absolute_pos) == 2:
        raise ValueError("RBS must be drawn with absolute_pos option set to a list of length 2.")
    if not isinstance(absolute_pos[0], int) or not isinstance(absolute_pos[1], int):
        raise ValueError("RBS must be drawn with absolute_pos option set to a list of integers.")

    # Check direction add start padding
    dir_fac = 1.0
    final_end = end
    final_start = prev_end


    if start > end:
        dir_fac = -1.0
        start = absolute_pos[0]
        end = absolute_pos[1]
    else:
        start = absolute_pos[0]
        end = absolute_pos[1]
        final_end = end+end_pad

    # Draw the CDS symbol
    if abs(start-end) <= arrowhead_length:
        p1 = Polygon([(start, y_extent+arrowhead_height),
                    (start, -y_extent-arrowhead_height),
                    (end, 0)],
                    edgecolor=edgecolor, facecolor=color, linewidth=linewidth, 
                    hatch=hatch, zorder=11+zorder_add, 
                    path_effects=[Stroke(joinstyle="miter")])
    else:
        p1 = Polygon([(start, y_extent), 
                    (start, -y_extent),
                    (end-dir_fac*arrowhead_length, -y_extent),
                    (end-dir_fac*arrowhead_length, -y_extent-arrowhead_height),
                    (end, 0),
                    (end-dir_fac*arrowhead_length, y_extent+arrowhead_height),
                    (end-dir_fac*arrowhead_length, y_extent)],
                    edgecolor=edgecolor, facecolor=color, linewidth=linewidth, 
                    hatch=hatch, zorder=11+zorder_add, 
                    path_effects=[Stroke(joinstyle="miter")]) # This is a work around for matplotlib < 1.4.0
    ax.add_patch(p1)


    if opts != None and 'label' in list(opts.keys()):
        dpl.write_label(ax, opts['label'], (start+end)/2, opts=opts)

    return prev_end, prev_end, 

def custom_promoter(ax, type, num, start, end, prev_end, linewidth, opts):
    """ Built-in SBOL promoter renderer.
    """
    # Additional Options
    zorder_add = opts.get('zorder_add', 0.0)
    color = opts.get('color', (0.0,0.0,0.0))
    start_pad = opts.get('start_pad', 2.0)
    end_pad = opts.get('end_pad', 2.0)
    y_extent = opts.get('y_extent', 10)
    x_extent = opts.get('x_extent', 10)
    arrowhead_height = opts.get('arrowhead_height', 2)
    arrowhead_length = opts.get('arrowhead_length', 4)
    linewidth = opts.get('linewidth', 1.0)

    absolute_pos = opts.get('absolute_pos', None)

    # Sanity Checking
    if not absolute_pos:
        raise ValueError("Promoter must be drawn with absolute_pos option set.")
    if not isinstance(absolute_pos, list):
        raise ValueError("Promoter must be drawn with absolute_pos option set to a list.")
    if not len(absolute_pos) == 2:
        raise ValueError("Promoter must be drawn with absolute_pos option set to a list of length 2.")
    if not isinstance(absolute_pos[0], int) or not isinstance(absolute_pos[1], int):
        raise ValueError("Promoter must be drawn with absolute_pos option set to a list of integers.")
    
    start = absolute_pos[0]
    end = absolute_pos[1]

    # Check direction add start padding
    dir_fac = 1.0
    final_end = end
    final_start = prev_end
    if start > end:
        dir_fac = -1.0
        start = prev_end+end_pad+x_extent
        end = prev_end+end_pad
        final_end = start+start_pad
    else:
        start = prev_end+start_pad
        end = start+x_extent
        final_end = end+end_pad
    # Draw the promoter symbol
    l1 = Line2D([start,start],[0,dir_fac*y_extent], linewidth=linewidth, 
                color=color, zorder=9+zorder_add)
    l2 = Line2D([start,start+dir_fac*x_extent-dir_fac*(arrowhead_length*0.5)],
                [dir_fac*y_extent,dir_fac*y_extent], linewidth=linewidth, 
                color=color, zorder=10+zorder_add)
    ax.add_line(l1)
    ax.add_line(l2)
    p1 = Polygon([(start+dir_fac*x_extent-dir_fac*arrowhead_length, 
                   dir_fac*y_extent+(arrowhead_height)), 
                  (start+dir_fac*x_extent, dir_fac*y_extent),
                  (start+dir_fac*x_extent-dir_fac*arrowhead_length, 
                   dir_fac*y_extent-(arrowhead_height))],
                  facecolor=color, edgecolor=color, linewidth=linewidth,  zorder=1+zorder_add,
                  path_effects=[Stroke(joinstyle="miter")]) # This is a work around for matplotlib < 1.4.0
    ax.add_patch(p1)
    if opts != None and 'label' in list(opts.keys()):
        if final_start > final_end:
            dpl.write_label(ax, opts['label'], final_end+((final_start-final_end)/2.0), opts=opts)
        else:
            dpl.write_label(ax, opts['label'], final_start+((final_end-final_start)/2.0), opts=opts)
    if final_start > final_end:
        return prev_end, final_start
    else:
        return prev_end, final_end

def custom_terminator():
    raise NotImplementedError("Terminator not yet implemented.")

def custom_annotation(ax, type, num, start, end, prev_end, scale, linewidth, opts):
    """ Built-in SBOL user-defined element renderer.
    """
    # Additional Options
    zorder_add = opts.get('zorder_add', 0.0)
    color = opts.get('color', (0,0,0))
    start_pad = opts.get('start_pad', 2.0)
    end_pad = opts.get('end_pad', 2.0)
    x_extent = opts.get('x_extent', 12.0)
    y_extent = opts.get('y_extent', 5.0)
    linestyle = opts.get('linestyle', '-')
    fill_color = opts.get('fill_color', (1,1,1))
    linewidth = opts.get('linewidth', 1.0)
    scale = opts.get('scale', 1.0)
    absolute_pos = opts.get('absolute_pos', None)
    y_offset = opts.get('y_offset', 0.0)

    # Sanity Checking
    if not absolute_pos:
        raise ValueError("Annotation must be drawn with absolute_pos option set.")
    if not isinstance(absolute_pos, list):
        raise ValueError("Annotation must be drawn with absolute_pos option set to a list.")
    if not len(absolute_pos) == 2:
        raise ValueError("Annotation must be drawn with absolute_pos option set to a list of length 2.")
    if not isinstance(absolute_pos[0], int) or not isinstance(absolute_pos[1], int):
        raise ValueError("Annotation must be drawn with absolute_pos option set to a list of integers.")
    


    # Check direction add start padding
    final_end = end
    final_start = prev_end

    start = absolute_pos[0]
    end = absolute_pos[1]
    final_end = end+end_pad
    
    #white rectangle overlays backbone line
    p1 = Polygon([(start, y_extent + y_offset), 
                  (start, -y_extent + y_offset),
                  (end, -y_extent + y_offset),
                  (end, y_extent + y_offset)],
                  edgecolor=color, facecolor=fill_color, linewidth=linewidth, zorder=11+zorder_add, 
                  path_effects=[Stroke(joinstyle="miter")]) # This is a work around for matplotlib < 1.4.0)     

    ax.add_patch(p1)
    
    if opts != None and 'label' in list(opts.keys()):
        label_position = (start+end)/2
        if final_start > final_end:
            dpl.write_label(ax, opts['label'], label_position, opts=opts)
        else:
            dpl.write_label(ax, opts['label'], label_position, opts=opts)

    if final_start > final_end:
        return prev_end, final_start
    else:
        return prev_end, final_end

