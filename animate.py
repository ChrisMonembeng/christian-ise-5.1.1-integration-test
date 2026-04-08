import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Plotly Animation Demo", layout="wide")

st.title("5 Plotly Animations in Streamlit")

animation_choice = st.selectbox(
    "Choose an animation",
    [
        "Rotating 3D Helix",
        "Moving Sine Wave",
        "Bouncing Ball",
        "Rippling 3D Surface",
        "Orbiting Planets",
    ],
)

num_frames = 60


def rotating_3d_helix():
    t = np.linspace(0, 8 * np.pi, 200)
    x = np.cos(t)
    y = np.sin(t)
    z = np.linspace(-2, 2, 200)

    frames = []
    for i in range(num_frames):
        angle = 2 * np.pi * i / num_frames
        x_rot = x * np.cos(angle) - y * np.sin(angle)
        y_rot = x * np.sin(angle) + y * np.cos(angle)

        frames.append(
            go.Frame(
                data=[
                    go.Scatter3d(
                        x=x_rot,
                        y=y_rot,
                        z=z,
                        mode="lines",
                    )
                ],
                name=str(i),
            )
        )

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
            )
        ],
        frames=frames,
    )

    fig.update_layout(
        title="Rotating 3D Helix",
        scene=dict(
            xaxis=dict(range=[-1.5, 1.5]),
            yaxis=dict(range=[-1.5, 1.5]),
            zaxis=dict(range=[-2.5, 2.5]),
            aspectmode="cube",
        ),
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 50, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                            },
                        ],
                    },
                ],
            }
        ],
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


def moving_sine_wave():
    x = np.linspace(0, 4 * np.pi, 300)

    frames = []
    for i in range(num_frames):
        phase = 2 * np.pi * i / num_frames
        y = np.sin(x + phase)

        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=x,
                        y=y,
                        mode="lines",
                    )
                ],
                name=str(i),
            )
        )

    fig = go.Figure(
        data=[
            go.Scatter(
                x=x,
                y=np.sin(x),
                mode="lines",
            )
        ],
        frames=frames,
    )

    fig.update_layout(
        title="Moving Sine Wave",
        xaxis=dict(range=[0, 4 * np.pi]),
        yaxis=dict(range=[-1.5, 1.5]),
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 50, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                            },
                        ],
                    },
                ],
            }
        ],
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


def bouncing_ball():
    x_positions = np.linspace(0, 10, num_frames)
    y_positions = np.abs(np.sin(np.linspace(0, 3 * np.pi, num_frames))) * 5

    frames = []
    for i in range(num_frames):
        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=[x_positions[i]],
                        y=[y_positions[i]],
                        mode="markers",
                        marker=dict(size=20),
                    )
                ],
                name=str(i),
            )
        )

    fig = go.Figure(
        data=[
            go.Scatter(
                x=[x_positions[0]],
                y=[y_positions[0]],
                mode="markers",
                marker=dict(size=20),
            )
        ],
        frames=frames,
    )

    fig.update_layout(
        title="Bouncing Ball",
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[0, 6]),
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 60, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                            },
                        ],
                    },
                ],
            }
        ],
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


def rippling_3d_surface():
    """
    A 3D surface that simulates a ripple/water-drop effect. Each frame advances
    the phase of a radially symmetric sine wave, making the rings appear to
    expand outward from the center.
    """
    grid_size = 50
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)  # distance from center for each grid point

    frames = []
    for i in range(num_frames):
        phase = 2 * np.pi * i / num_frames
        # Amplitude fades with distance so the edges stay calm
        Z = np.sin(R * 2 - phase) * np.exp(-R * 0.3)
        frames.append(
            go.Frame(
                data=[
                    go.Surface(
                        z=Z,
                        x=X,
                        y=Y,
                        colorscale="Blues",
                        cmin=-1,
                        cmax=1,
                        showscale=False,
                    )
                ],
                name=str(i),
            )
        )

    Z_init = np.sin(R * 2) * np.exp(-R * 0.3)
    fig = go.Figure(
        data=[
            go.Surface(
                z=Z_init,
                x=X,
                y=Y,
                colorscale="Blues",
                cmin=-1,
                cmax=1,
                showscale=False,
            )
        ],
        frames=frames,
    )

    fig.update_layout(
        title="Rippling 3D Surface",
        scene=dict(
            xaxis=dict(range=[-5, 5], showticklabels=False),
            yaxis=dict(range=[-5, 5], showticklabels=False),
            zaxis=dict(range=[-1.2, 1.2]),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.0)),
        ),
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 50, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                            },
                        ],
                    },
                ],
            }
        ],
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


def orbiting_planets():
    """
    Three planets orbiting a central star at different speeds and radii.
    Each planet leaves a faint trail showing its full orbit path.
    """
    # Orbital parameters: (radius, angular_speed, color, size, name)
    planets = [
        (1.5, 3.0, "deepskyblue",  12, "Mercury"),
        (3.0, 1.5, "orange",        16, "Venus"),
        (5.0, 0.8, "limegreen",     14, "Earth"),
    ]

    theta = np.linspace(0, 2 * np.pi, 200)

    frames = []
    for i in range(num_frames):
        frame_data = []

        # Draw orbit rings (static faint circles)
        for radius, *_ in planets:
            frame_data.append(
                go.Scatter(
                    x=radius * np.cos(theta),
                    y=radius * np.sin(theta),
                    mode="lines",
                    line=dict(color="rgba(200,200,200,0.25)", width=1),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        # Draw the central star
        frame_data.append(
            go.Scatter(
                x=[0],
                y=[0],
                mode="markers",
                marker=dict(size=28, color="yellow", symbol="circle",
                            line=dict(color="orange", width=2)),
                name="Star",
                showlegend=False,
            )
        )

        # Draw each planet at its current position
        for radius, speed, color, size, name in planets:
            angle = 2 * np.pi * i / num_frames * speed
            px = radius * np.cos(angle)
            py = radius * np.sin(angle)
            frame_data.append(
                go.Scatter(
                    x=[px],
                    y=[py],
                    mode="markers",
                    marker=dict(size=size, color=color,
                                line=dict(color="white", width=1)),
                    name=name,
                    showlegend=(i == 0),
                )
            )

        frames.append(go.Frame(data=frame_data, name=str(i)))

    # Build the initial figure using frame 0's data
    fig = go.Figure(data=frames[0].data, frames=frames)

    fig.update_layout(
        title="Orbiting Planets",
        xaxis=dict(range=[-6.5, 6.5], showgrid=False,
                   zeroline=False, showticklabels=False),
        yaxis=dict(range=[-6.5, 6.5], showgrid=False,
                   zeroline=False, showticklabels=False,
                   scaleanchor="x", scaleratio=1),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        legend=dict(x=1.02, y=0.5, font=dict(color="white")),
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 60, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                            },
                        ],
                    },
                ],
                "font": {"color": "black"},
            }
        ],
        margin=dict(l=0, r=120, t=50, b=0),
    )
    return fig


if animation_choice == "Rotating 3D Helix":
    fig = rotating_3d_helix()
elif animation_choice == "Moving Sine Wave":
    fig = moving_sine_wave()
elif animation_choice == "Bouncing Ball":
    fig = bouncing_ball()
elif animation_choice == "Rippling 3D Surface":
    fig = rippling_3d_surface()
else:
    fig = orbiting_planets()

st.plotly_chart(fig, use_container_width=True)