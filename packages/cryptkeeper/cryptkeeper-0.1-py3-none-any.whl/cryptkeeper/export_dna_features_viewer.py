# Concept for visualizing cryptkeeper output with DNA features viewer

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from dna_features_viewer import BiopythonTranslator, GraphicRecord, GraphicFeature
from Bio import SeqIO
import numpy as np
from .export import CDS_COLOR
from bokeh.plotting import show
from .helpers import gradient_color, gradient_color_matplotlib

COLORMAP = 'viridis'

def _profile_features(cryptresult) -> dict:
    features = {'framef0': [],
                'framef1': [],
                'framef2': [],
                'framer0': [],
                'framer1': [],
                'framer2': []}
    
    for feature in cryptresult.translation_sites:
        # Set up the feature for graphing
        part_design = {"start": feature.start,
                       "end": feature.end,
                       "type": "CDS",
                       "strand": "fwd",
                       "opts": {"color": CDS_COLOR},
                       "strength": feature.burden}

        # Determine the strand
        strand = feature.strand
        if strand == "+":
            frame = feature.start % 3
        elif strand == "-":
            frame = (len(cryptresult.sequence) - feature.end) % 3
        else:
            raise ValueError("Strand must be + or -")
        

        # Assign the part to a frame

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

        # Add the part to the frame
        if abs(feature.start - feature.end) < 60:
            continue
        features[frame_tgt].append(part_design)
    return features
        

def plot_features_viewer(cryptresult, genbank_file=None):

    # Set up plot

    if genbank_file:
        fig, axis = plt.subplots(
        2, 1, figsize=(15, 25), sharex=False, gridspec_kw={"height_ratios": [2, 10]}, constrained_layout=True)
        (axis_annotations, axis_predictions) = axis
    else:
        fig, axis = plt.subplots(
        2, 1, figsize=(15, 25), sharex=False, gridspec_kw={"height_ratios": [2, 10]}, constrained_layout=True)
        (axis_annotations, axis_predictions) = axis


    # Do Annotation Axis
    annotation_features = []
    for annotation in cryptresult.annotations:
        annotation_features.append(GraphicFeature(start=annotation.start, end=annotation.end, strand=annotation.strand, color=annotation.color, label=annotation.name))
    record = GraphicRecord(features=annotation_features, sequence_length=len(cryptresult.sequence))
    record.plot(ax=axis_annotations, with_ruler=True, draw_line=True)



    # Profile features from cryptresult
    features = _profile_features(cryptresult)

    # Unnest features to one frame
    features = {"frame": [feature for frame in features.values() for feature in frame]}

    # Set colors
    min_strength = min([feature['strength'] for feature in features['frame']])
    max_strength = max([feature['strength'] for feature in features['frame']])
    color_generator = gradient_color_matplotlib(COLORMAP, 1, max_strength, log=False, type="hex")
    for feature in features['frame']:
        feature['opts']['color'] = color_generator(feature['strength'])

    for frame_key, plot_axis in zip(features.keys(), [axis_predictions]):
        frame_data = features[frame_key]
        converted_features = []
        for feature in frame_data:
            feature_strand = -1 if feature['strand'] == "+" else +1
            converted_features.append(GraphicFeature(start=feature['start'], end=feature['end'], strand=feature_strand, color=feature['opts']['color']))
        record = GraphicRecord(sequence=cryptresult.sequence, features=converted_features)
        record.feature_level_height = 0.3
        record.plot(ax=plot_axis, with_ruler=False, draw_line=False)

    # Flip prediction axis
    axis_predictions.set_ylim(axis_predictions.get_ylim()[::-1])

    # Add a color bar to the plot
    sm = plt.cm.ScalarMappable(cmap=COLORMAP, norm=colors.Normalize(vmin=1, vmax=max_strength))
    cbar = plt.colorbar(sm, ax=axis[:], shrink=0.5, aspect=10)
    cbar.set_label('Burden of Expression')


    return fig

# EOF
