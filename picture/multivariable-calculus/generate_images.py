"""Generate mathematical diagrams for MIT 18.024 blog series."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Arc, Circle, Polygon
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Use a style that looks clean and modern
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches='tight', pad_inches=0.1, facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved: {name}")

# ============================================================
# Blog 1: Linear Algebra Foundations
# ============================================================

def blog1_images():
    print("Blog 1: Linear Algebra Foundations")

    # 1.1 Subspaces in R3
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5),
                              subplot_kw={'projection': '3d'})
    titles = ['Line through origin (1D subspace)',
              'Plane through origin (2D subspace)',
              'Plane NOT through origin\n(NOT a subspace)']
    for ax, title in zip(axes, titles):
        ax.set_title(title, fontsize=11)
        ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
        ax.set_xlim(-2,2); ax.set_ylim(-2,2); ax.set_zlim(-2,2)

    # Line: x=t, y=2t, z=-t
    t = np.linspace(-2, 2, 100)
    axes[0].plot(t, 2*t, -t, 'b-', linewidth=2)
    axes[0].scatter([0],[0],[0], c='r', s=50)

    # Plane through origin: x+y-z=0
    xx, yy = np.meshgrid(np.linspace(-2,2,10), np.linspace(-2,2,10))
    zz = xx + yy
    axes[1].plot_surface(xx, yy, zz, alpha=0.4, color='blue')
    axes[1].scatter([0],[0],[0], c='r', s=50)

    # Plane NOT through origin: x+y-z=2
    zz2 = xx + yy - 2
    axes[2].plot_surface(xx, yy, zz2, alpha=0.4, color='orange')
    axes[2].scatter([0],[0],[0], c='r', s=50, marker='x')

    save(fig, '01-subspaces-r3.png')

    # 1.2 Basis vectors in R3
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'projection': '3d'})
    ax.set_title('Standard Basis in $\\mathbb{R}^3$', fontsize=13)
    ax.set_xlim(0,1.5); ax.set_ylim(0,1.5); ax.set_zlim(0,1.5)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    colors = ['#e74c3c', '#2ecc71', '#3498db']
    labels = ['$\\mathbf{i}=(1,0,0)$', '$\\mathbf{j}=(0,1,0)$', '$\\mathbf{k}=(0,0,1)$']
    origins = [(0,0,0)]*3
    vecs = [(1,0,0), (0,1,0), (0,0,1)]
    for o, v, c, l in zip(origins, vecs, colors, labels):
        ax.quiver(*o, *v, color=c, linewidth=3, arrow_length_ratio=0.15, label=l)
    # Show an arbitrary vector as combination
    v_arb = (0.8, 1.2, 0.6)
    ax.quiver(0,0,0, *v_arb, color='purple', linewidth=2, arrow_length_ratio=0.15,
              label='$0.8\\mathbf{i}+1.2\\mathbf{j}+0.6\\mathbf{k}$', alpha=0.7)
    # Dashed projection lines
    ax.plot([0.8,0.8],[0,1.2],[0,0], 'gray', linestyle='--', alpha=0.3)
    ax.plot([0,0.8],[1.2,1.2],[0,0], 'gray', linestyle='--', alpha=0.3)
    ax.plot([0.8,0.8],[1.2,1.2],[0,0.6], 'gray', linestyle='--', alpha=0.3)
    ax.legend(fontsize=10)
    save(fig, '01-basis-vectors-r3.png')

    # 1.3 Linear transformation: rotation + scaling
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    # Create a grid and some shapes in the domain
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x, circle_y = np.cos(theta), np.sin(theta)
    square = np.array([[1,1],[1,-1],[-1,-1],[-1,1],[1,1]])
    # Domain
    axes[0].set_title('Domain: unit circle + square', fontsize=12)
    axes[0].plot(circle_x, circle_y, 'b-', linewidth=2)
    axes[0].plot(square[:,0], square[:,1], 'r-', linewidth=2)
    axes[0].axhline(0, color='gray', alpha=0.3); axes[0].axvline(0, color='gray', alpha=0.3)
    axes[0].set_xlim(-3,3); axes[0].set_ylim(-3,3)
    axes[0].set_aspect('equal'); axes[0].grid(True, alpha=0.3)
    # Codomain: after T = [[2,1],[0,2]] (shear + scale)
    T = np.array([[2,1],[0,2]])
    circ_trans = T @ np.vstack([circle_x, circle_y])
    sq_trans = T @ square.T
    axes[1].set_title('Image under T = [[2,1],[0,2]]', fontsize=12)
    axes[1].plot(circ_trans[0], circ_trans[1], 'b-', linewidth=2)
    axes[1].plot(sq_trans[0], sq_trans[1], 'r-', linewidth=2)
    axes[1].axhline(0, color='gray', alpha=0.3); axes[1].axvline(0, color='gray', alpha=0.3)
    axes[1].set_xlim(-3,3); axes[1].set_ylim(-3,3)
    axes[1].set_aspect('equal'); axes[1].grid(True, alpha=0.3)
    fig.suptitle('Linear Transformation: Geometry', fontsize=14, y=1.02)
    save(fig, '01-linear-transformation-geometry.png')

    # 1.4 Determinant as volume
    fig, ax = plt.subplots(figsize=(8, 7), subplot_kw={'projection': '3d'})
    ax.set_title('Determinant = Volume of Parallelepiped\n$\\det[\\mathbf{a}\\;\\mathbf{b}\\;\\mathbf{c}]$', fontsize=13)
    a, b, c = np.array([2,0,0]), np.array([0.5,1.5,0]), np.array([0.3,0.4,1.5])
    origin = np.zeros(3)
    for v, col, lbl in [(a,'#e74c3c','a'), (b,'#2ecc71','b'), (c,'#3498db','c')]:
        ax.quiver(*origin, *v, color=col, linewidth=3, arrow_length_ratio=0.1, label=f'${lbl}$')
    # Draw the parallelepiped
    verts = [
        [origin, a, a+b, b],
        [origin, a, a+c, c],
        [origin, b, b+c, c],
        [a, a+b, a+b+c, a+c],
        [b, a+b, a+b+c, b+c],
        [c, a+c, a+b+c, b+c],
    ]
    for face in verts[:3]:
        poly = Poly3DCollection([face], alpha=0.15, color='gray', edgecolor='gray', linewidth=0.5)
        ax.add_collection3d(poly)
    ax.set_xlim(0,2.5); ax.set_ylim(0,2); ax.set_zlim(0,2)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.legend(fontsize=9)
    save(fig, '01-determinant-volume.png')

    # 1.5 Cross product geometry
    fig, ax = plt.subplots(figsize=(8, 7), subplot_kw={'projection': '3d'})
    ax.set_title('Cross Product $\\mathbf{a}\\times\\mathbf{b}$\n(perpendicular to both, area = $\\|\\mathbf{a}\\|\\|\\mathbf{b}\\|\\sin\\theta$)', fontsize=12)
    a3, b3 = np.array([2,0.3,0]), np.array([0.5,1.5,0])
    cross = np.cross(a3, b3)
    origin = np.zeros(3)
    ax.quiver(*origin, *a3, color='#e74c3c', linewidth=3, arrow_length_ratio=0.1, label='$\\mathbf{a}$')
    ax.quiver(*origin, *b3, color='#2ecc71', linewidth=3, arrow_length_ratio=0.1, label='$\\mathbf{b}$')
    ax.quiver(*origin, *cross, color='#9b59b6', linewidth=3, arrow_length_ratio=0.1, label='$\\mathbf{a}\\times\\mathbf{b}$')
    # Parallelogram
    pts = np.array([origin, a3, a3+b3, b3, origin])
    ax.plot(pts[:,0], pts[:,1], pts[:,2], 'gray', linewidth=1, alpha=0.5)
    poly = Poly3DCollection([[origin, a3, a3+b3, b3]], alpha=0.2, color='gray')
    ax.add_collection3d(poly)
    ax.set_xlim(0,2.5); ax.set_ylim(0,2); ax.set_zlim(0,2)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.legend(fontsize=10)
    save(fig, '01-cross-product-geometry.png')


# ============================================================
# Blog 2: Vector Functions and Space Curves
# ============================================================

def blog2_images():
    print("Blog 2: Vector Functions & Space Curves")

    # 2.1 Space curve: helix
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Space Curve: Helix $\\mathbf{r}(t)=(\\cos t,\\sin t,t)$\nwith tangent vectors', fontsize=13)
    t = np.linspace(0, 4*np.pi, 300)
    x, y, z = np.cos(t), np.sin(t), t/(2*np.pi)
    ax.plot(x, y, z, 'b-', linewidth=2)
    # Tangent vectors at selected points
    for t0 in [np.pi/2, np.pi, 3*np.pi/2, 2*np.pi, 5*np.pi/2, 3*np.pi]:
        p = np.array([np.cos(t0), np.sin(t0), t0/(2*np.pi)])
        v = np.array([-np.sin(t0), np.cos(t0), 1/(2*np.pi)])
        v = v / np.linalg.norm(v) * 0.4
        ax.quiver(*p, *v, color='r', linewidth=2, arrow_length_ratio=0.3)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.5,1.5); ax.set_zlim(0,2.5)
    save(fig, '02-helix-tangent.png')

    # 2.2 Curvature: circles of different radii
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    configs = [
        (1.0, 'Circle radius $R=1$\n$\\kappa=1/R=1$'),
        (2.0, 'Circle radius $R=2$\n$\\kappa=1/R=0.5$'),
        (0.5, 'Circle radius $R=0.5$\n$\\kappa=1/R=2$'),
    ]
    for ax, (R, title) in zip(axes, configs):
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(R*np.cos(theta), R*np.sin(theta), 'b-', linewidth=3)
        # Osculating circle at a point
        t0 = np.pi/4
        px, py = R*np.cos(t0), R*np.sin(t0)
        ax.scatter([px], [py], c='r', s=60, zorder=5)
        # Tangent line
        tx, ty = -np.sin(t0), np.cos(t0)
        tl = 0.8
        ax.plot([px-tl*tx, px+tl*tx], [py-tl*ty, py+tl*ty], 'r--', linewidth=1.5, alpha=0.7)
        # Normal (points to center)
        ax.plot([px, 0], [py, 0], 'g--', linewidth=1, alpha=0.5)
        ax.set_title(title, fontsize=11)
        ax.set_aspect('equal')
        ax.set_xlim(-2.5,2.5); ax.set_ylim(-2.5,2.5)
        ax.axhline(0,color='gray',alpha=0.2); ax.axvline(0,color='gray',alpha=0.2)
        ax.grid(True, alpha=0.3)
    fig.suptitle('Curvature: Smaller radius = Larger curvature', fontsize=14, y=1.02)
    save(fig, '02-curvature-circles.png')

    # 2.3 Kepler's laws illustration
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.set_title("Kepler's First Law: Elliptical Orbit\n(Sun at one focus)", fontsize=13)
    a, b = 3, 2
    c = np.sqrt(a**2 - b**2)
    theta = np.linspace(0, 2*np.pi, 300)
    x, y = a*np.cos(theta), b*np.sin(theta)
    ax.plot(x, y, 'b-', linewidth=2.5, label='Planetary orbit')
    ax.scatter([0], [0], c='gray', s=200, marker='o', zorder=5, label='Empty focus')
    ax.scatter([c], [0], c='#f39c12', s=300, marker='o', zorder=5, label='Sun (focus)')
    # Equal area in equal time
    for t0, col in [(0, 'red'), (np.pi/2, 'green'), (np.pi, 'purple')]:
        t_range = np.linspace(t0, t0+np.pi/4, 50)
        x_seg = a*np.cos(t_range); y_seg = b*np.sin(t_range)
        ax.fill(np.concatenate([[c], x_seg, [c]]),
                np.concatenate([[0], y_seg, [0]]),
                alpha=0.15, color=col)
    ax.set_aspect('equal')
    ax.set_xlim(-4,5); ax.set_ylim(-3,3)
    ax.legend(fontsize=10); ax.grid(True, alpha=0.3)
    save(fig, '02-kepler-orbit.png')

    # 2.4 Polar coordinates: cardioid
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'projection': 'polar'})
    ax.set_title('Cardioid: $r = 1 + \\cos\\theta$', fontsize=13, pad=20)
    theta = np.linspace(0, 2*np.pi, 400)
    r = 1 + np.cos(theta)
    ax.plot(theta, r, 'b-', linewidth=2.5)
    ax.fill(theta, r, alpha=0.1, color='blue')
    save(fig, '02-cardioid-polar.png')


# ============================================================
# Blog 3: Multivariable Differential Calculus
# ============================================================

def blog3_images():
    print("Blog 3: Multivariable Differential Calculus")

    # 3.1 Gradient field + contour plot
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.set_title('Gradient Field of $f(x,y)=x^2+y^2$\n(perpendicular to level sets)', fontsize=13)
    x = np.linspace(-2, 2, 20); y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    # Contours
    cs = ax.contour(X, Y, Z, levels=np.arange(0, 8.5, 0.5), colors='blue', alpha=0.5, linewidths=0.8)
    ax.clabel(cs, inline=True, fontsize=7, fmt='%.1f')
    # Gradient vectors
    xg = np.linspace(-2, 2, 12); yg = np.linspace(-2, 2, 12)
    Xg, Yg = np.meshgrid(xg, yg)
    U, V = 2*Xg, 2*Yg
    ax.quiver(Xg, Yg, U, V, angles='xy', scale_units='xy', scale=8, color='red', alpha=0.7, width=0.003)
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_aspect('equal'); ax.grid(True, alpha=0.3)
    save(fig, '03-gradient-contour.png')

    # 3.2 Tangent plane to a surface
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Tangent Plane to $z = x^2 + y^2$ at $(1,1,2)$', fontsize=13)
    x = np.linspace(-2, 2, 50); y = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    ax.plot_surface(X, Y, Z, alpha=0.4, cmap='Blues_r')
    # Tangent plane at (1,1,2): z = 2 + 2(x-1) + 2(y-1) = 2x + 2y - 2
    tx = np.linspace(0, 2, 20); ty = np.linspace(0, 2, 20)
    TX, TY = np.meshgrid(tx, ty)
    TZ = 2*TX + 2*TY - 2
    ax.plot_surface(TX, TY, TZ, alpha=0.6, color='orange')
    ax.scatter([1], [1], [2], c='r', s=80, marker='o')
    # Gradient vector (normal)
    ax.quiver(1, 1, 2, 0.3, 0.3, 1, color='red', linewidth=3, arrow_length_ratio=0.2, label='$\\nabla f(1,1)=(2,2)$')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.legend(fontsize=10)
    save(fig, '03-tangent-plane.png')

    # 3.3 Chain rule visualization
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_title('Chain Rule: Composition Tree\n$h(x,y)=f(u(x,y), v(x,y))$', fontsize=13)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis('off')
    # Draw nodes and edges
    nodes = {'h': (5, 9), 'u': (3, 5.5), 'v': (7, 5.5), 'x': (2.5, 2.5), 'y': (7.5, 2.5)}
    for n, (nx, ny) in nodes.items():
        circle = Circle((nx, ny), 0.4, color='#3498db', alpha=0.2)
        ax.add_patch(circle)
        ax.text(nx, ny, f'${n}$', ha='center', va='center', fontsize=14, fontweight='bold')
    edges = [('h','u'), ('h','v'), ('u','x'), ('u','y'), ('v','x'), ('v','y')]
    for s, t in edges:
        sx, sy = nodes[s]; tx, ty = nodes[t]
        ax.annotate('', xy=(tx, ty), xytext=(sx, sy),
                     arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
    # Labels on edges
    ax.text(3.2, 7.2, '$\\frac{\\partial f}{\\partial u}$', fontsize=10, color='#e74c3c')
    ax.text(6.8, 7.2, '$\\frac{\\partial f}{\\partial v}$', fontsize=10, color='#e74c3c')
    ax.text(3.7, 4, '$\\frac{\\partial u}{\\partial x}$', fontsize=10, color='#2ecc71')
    ax.text(2.3, 4, '$\\frac{\\partial u}{\\partial y}$', fontsize=10, color='#2ecc71')
    ax.text(6.3, 4, '$\\frac{\\partial v}{\\partial x}$', fontsize=10, color='#2ecc71')
    ax.text(7.7, 4, '$\\frac{\\partial v}{\\partial y}$', fontsize=10, color='#2ecc71')
    ax.text(5, 1.2,
            '$\\frac{\\partial h}{\\partial x} = \\frac{\\partial f}{\\partial u}\\frac{\\partial u}{\\partial x} + \\frac{\\partial f}{\\partial v}\\frac{\\partial v}{\\partial x}$',
            ha='center', fontsize=13, family='monospace')
    save(fig, '03-chain-rule-tree.png')


# ============================================================
# Blog 4: Optimization & Implicit Function Theorem
# ============================================================

def blog4_images():
    print("Blog 4: Optimization & Implicit Function Theorem")

    # 4.1 Saddle point: f(x,y) = x^2 - y^2
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Saddle Point: $f(x,y)=x^2-y^2$ at $(0,0)$\n(min along x, max along y)', fontsize=13)
    x = np.linspace(-2, 2, 80); y = np.linspace(-2, 2, 80)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2
    ax.plot_surface(X, Y, Z, alpha=0.7, cmap='RdBu_r')
    # Highlight the saddle
    ax.scatter([0], [0], [0], c='yellow', s=100, marker='o', edgecolors='black', linewidth=1)
    # Trace along x-axis and y-axis
    ax.plot(x, np.zeros_like(x), x**2, 'g-', linewidth=3, label='Along $x$-axis: $f(x,0)=x^2$ (min)')
    ax.plot(np.zeros_like(y), y, -y**2, 'r-', linewidth=3, label='Along $y$-axis: $f(0,y)=-y^2$ (max)')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.legend(fontsize=10)
    save(fig, '04-saddle-point.png')

    # 4.2 Lagrange multiplier geometry
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_title('Lagrange Multiplier Geometry\n$\\nabla f = \\lambda \\nabla g$ at constrained extremum', fontsize=13)
    ax.set_xlim(-2, 2.5); ax.set_ylim(-2, 2.5)
    ax.set_aspect('equal')

    # Constraint: unit circle x^2+y^2=1
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), 'b-', linewidth=2.5, label='Constraint $g=x^2+y^2-1=0$')

    # Objective contours: f(x,y) = xy
    x = np.linspace(-2, 2.5, 100); y = np.linspace(-2, 2.5, 100)
    X, Y = np.meshgrid(x, y)
    Z = X * Y
    levels = [-1.0, -0.5, -0.25, 0, 0.25, 0.5, 1.0]
    cs = ax.contour(X, Y, Z, levels=levels, colors='red', alpha=0.5, linewidths=1)
    ax.clabel(cs, inline=True, fontsize=8)

    # At extremum point (1/sqrt(2), 1/sqrt(2)):
    px, py = 1/np.sqrt(2), 1/np.sqrt(2)
    ax.scatter([px, -px, -px, px], [py, py, -py, -py], c='purple', s=80, zorder=5)
    # Gradient vectors at tangency point
    gf = np.array([py, px]); gg = np.array([2*px, 2*py])
    scale = 0.4
    ax.quiver(px, py, scale*gf[0], scale*gf[1], angles='xy', scale_units='xy', scale=1,
              color='red', linewidth=2, label='$\\nabla f$')
    ax.quiver(px, py, scale*gg[0]/np.linalg.norm(gg), scale*gg[1]/np.linalg.norm(gg),
              angles='xy', scale_units='xy', scale=1, color='blue', linewidth=2, label='$\\nabla g$')
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)
    save(fig, '04-lagrange-multiplier.png')


# ============================================================
# Blog 5: Line Integrals & Conservative Fields
# ============================================================

def blog5_images():
    print("Blog 5: Line Integrals & Conservative Fields")

    # 5.1 Vector field with multiple paths
    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_title('Line Integral: Path Dependence\n$\\int_C \\mathbf{F}\\cdot d\\mathbf{r}$ depends on $C$', fontsize=13)
    x = np.linspace(0, 3, 15); y = np.linspace(0, 3, 15)
    X, Y = np.meshgrid(x, y)
    U, V = X*Y, X + Y
    ax.quiver(X, Y, U, V, alpha=0.4, color='gray', width=0.002)
    # Three paths from (0,0) to (2,2)
    t = np.linspace(0, 1, 100)
    paths = [
        (2*t, 2*t, 'Direct line', 'blue'),
        (2*t, 2*t**2, 'Parabola', 'red'),
        (2*np.sin(np.pi*t/2), 2*t, 'Curved', 'green'),
    ]
    for px, py, lbl, col in paths:
        ax.plot(px, py, color=col, linewidth=2.5, label=f'Path: {lbl}')
    ax.scatter([0,2], [0,2], c='black', s=80, zorder=5)
    ax.text(-0.1, -0.1, 'A(0,0)', fontsize=11); ax.text(2, 2.1, 'B(2,2)', fontsize=11)
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_xlim(-0.3,3); ax.set_ylim(-0.3,3)
    ax.set_aspect('equal'); ax.legend(fontsize=10); ax.grid(True, alpha=0.3)
    save(fig, '05-line-integral-paths.png')

    # 5.2 Conservative vector field: gradient field with equipotential lines
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.set_title('Conservative Field $\\mathbf{F}=\\nabla\\varphi$\nPath independent: depends only on endpoints', fontsize=13)
    x = np.linspace(-2, 2, 16); y = np.linspace(-2, 2, 16)
    X, Y = np.meshgrid(x, y)
    # F = grad(x^2+y^2) = (2x, 2y)
    U, V = 2*X, 2*Y
    ax.quiver(X, Y, U, V, color='blue', alpha=0.6, width=0.003)
    # Equipotential contours
    xx = np.linspace(-2, 2, 100); yy = np.linspace(-2, 2, 100)
    XX, YY = np.meshgrid(xx, yy)
    ax.contour(XX, YY, XX**2+YY**2, levels=np.arange(0,8.5,0.5), colors='red', alpha=0.4, linewidths=0.8)
    # Two paths with same endpoints
    t = np.linspace(0, 1, 100)
    ax.plot(0.2+1.6*t, 0.2+1.6*t, 'g-', linewidth=2.5, label='Path 1')
    ax.plot(1.8*np.sin(np.pi*t/2)+0.2, 1.8*np.cos(np.pi*t/2)-0.8, 'purple', linewidth=2.5, label='Path 2')
    ax.scatter([0.2,1.8], [0.2,1.8], c='black', s=60, zorder=5)
    ax.set_aspect('equal'); ax.legend(fontsize=10); ax.grid(True, alpha=0.3)
    save(fig, '05-conservative-field.png')


# ============================================================
# Blog 6: Multiple Integrals
# ============================================================

def blog6_images():
    print("Blog 6: Multiple Integrals")

    # 6.1 Riemann sum approximation of double integral
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Double Integral as Limit of Riemann Sums\n$\\iint_R f(x,y)\\,dA$', fontsize=13)
    # Surface z = 4 - x^2 - y^2 over [-1.5, 1.5] x [-1.5, 1.5]
    x = np.linspace(-1.5, 1.5, 60); y = np.linspace(-1.5, 1.5, 60)
    X, Y = np.meshgrid(x, y)
    Z = 4 - X**2 - Y**2
    ax.plot_surface(X, Y, Z, alpha=0.4, cmap='Blues_r')
    # Show some partition boxes
    for xi in np.linspace(-1.25, 1.25, 6):
        for yi in np.linspace(-1.25, 1.25, 6):
            dx = 0.4; dy = 0.4
            z_val = max(0, 4 - xi**2 - yi**2)
            ax.bar3d(xi, yi, 0, dx, dy, z_val, alpha=0.3, color='orange', edgecolor='black', linewidth=0.3)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    save(fig, '06-riemann-sum.png')

    # 6.2 Integration over general region
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.set_title('Double Integral over General Region\n$x$-simple: $g_1(x) \\leq y \\leq g_2(x)$', fontsize=13)
    x = np.linspace(0, 2, 200)
    y_lower = x**2
    y_upper = 2*x
    ax.fill_between(x, y_lower, y_upper, alpha=0.3, color='blue')
    ax.plot(x, y_lower, 'b-', linewidth=2, label='$y=x^2$')
    ax.plot(x, y_upper, 'r-', linewidth=2, label='$y=2x$')
    # Show a vertical slice
    x0 = 1.0
    ax.plot([x0, x0], [x0**2, 2*x0], 'purple', linewidth=2.5, label=f'Slice at $x={x0}$')
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_xlim(-0.1, 2.2); ax.set_ylim(-0.1, 4.2)
    ax.set_aspect('equal')
    ax.legend(fontsize=10); ax.grid(True, alpha=0.3)
    save(fig, '06-general-region.png')


# ============================================================
# Blog 7: Green's Theorem & Change of Variables
# ============================================================

def blog7_images():
    print("Blog 7: Green's Theorem & Change of Variables")

    # 7.1 Green's Theorem: circulation around boundary = sum of micro-circulations
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    # Left: vector field along boundary
    ax = axes[0]
    ax.set_title("Green's Theorem: Boundary Circulation", fontsize=12)
    theta = np.linspace(0, 2*np.pi, 200)
    rx, ry = 2*np.cos(theta), np.sin(theta)  # ellipse
    ax.plot(rx, ry, 'b-', linewidth=2.5)
    # Show vector field F = (-y, x) along boundary
    for t0 in np.linspace(0, 2*np.pi, 20):
        px, py = 2*np.cos(t0), np.sin(t0)
        fx, fy = -py, px
        nrm = np.sqrt(fx**2+fy**2)
        ax.quiver(px, py, fx/nrm*0.4, fy/nrm*0.4, angles='xy', scale_units='xy', scale=1,
                  color='red', alpha=0.7, width=0.01)
    ax.set_aspect('equal'); ax.set_xlim(-2.5,2.5); ax.set_ylim(-2,2); ax.grid(True, alpha=0.3)

    # Right: curl field inside domain
    ax = axes[1]
    ax.set_title('Curl $Q_x-P_y$ integrated over region', fontsize=12)
    x = np.linspace(-2.2, 2.2, 15); y = np.linspace(-1.2, 1.2, 15)
    X, Y = np.meshgrid(x, y)
    ax.quiver(X, Y, -Y, X, alpha=0.4, color='gray', width=0.002)
    # interior of ellipse
    theta_fill = np.linspace(0, 2*np.pi, 200)
    ax.fill(2*np.cos(theta_fill), np.sin(theta_fill), alpha=0.15, color='blue')
    ax.set_aspect('equal'); ax.set_xlim(-2.5,2.5); ax.set_ylim(-2,2); ax.grid(True, alpha=0.3)
    fig.suptitle("Green's Theorem: $\\oint_C \\mathbf{F}\\cdot d\\mathbf{r} = \\iint_D (Q_x-P_y)\\,dA$", fontsize=14, y=1.03)
    save(fig, '07-greens-theorem.png')

    # 7.2 Change of variables: polar coordinates grid
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    # Left: polar grid in r,theta
    ax = axes[0]
    ax.set_title('Parameter Domain $(r,\\theta)$', fontsize=12)
    r_vals = np.linspace(0.2, 2, 5); t_vals = np.linspace(0, 2*np.pi, 13)
    for r in r_vals:
        ax.plot(r*np.cos(t_vals), r*np.sin(t_vals), 'b-', alpha=0.5, linewidth=0.8)
    for t in t_vals:
        ax.plot([0, 2*np.cos(t)], [0, 2*np.sin(t)], 'r-', alpha=0.5, linewidth=0.8)
    ax.set_aspect('equal'); ax.set_xlim(-2.2,2.2); ax.set_ylim(-2.2,2.2)
    ax.set_xlabel('$r\\cos\\theta$'); ax.set_ylabel('$r\\sin\\theta$')
    ax.grid(True, alpha=0.3)

    # Right: mapped (distorted grid in x,y)
    ax = axes[1]
    ax.set_title('Image Domain $(x,y)$ after transformation', fontsize=12)
    # Sample points in polar coords and map to cartesian
    # Just plot concentric circles and radial lines (which is what polar looks like)
    for r in r_vals:
        ax.plot(r*np.cos(t_vals), r*np.sin(t_vals), 'b-', alpha=0.5, linewidth=0.8)
    for t in t_vals:
        ax.plot([0, 2*np.cos(t)], [0, 2*np.sin(t)], 'r-', alpha=0.5, linewidth=0.8)
    # Highlight a small cell
    r0, t0 = 1.0, np.pi/6
    dr, dt = 0.3, 0.3
    cell_r = [r0, r0, r0+dr, r0+dr, r0]
    cell_t = [t0, t0+dt, t0+dt, t0, t0]
    ax.fill([rr*np.cos(tt) for rr,tt in zip(cell_r, cell_t)],
            [rr*np.sin(tt) for rr,tt in zip(cell_r, cell_t)],
            alpha=0.4, color='orange', edgecolor='red', linewidth=2)
    ax.text(1.2, 0.7, '$dA = r\\,dr\\,d\\theta$', fontsize=13, color='red', fontweight='bold')
    ax.set_aspect('equal'); ax.set_xlim(-2.2,2.2); ax.set_ylim(-2.2,2.2)
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.grid(True, alpha=0.3)
    fig.suptitle('Polar Coordinates: $dA = r\\,dr\\,d\\theta$', fontsize=14, y=1.02)
    save(fig, '07-polar-jacobian.png')


# ============================================================
# Blog 8: Surface Integrals & Vector Theorems
# ============================================================

def blog8_images():
    print("Blog 8: Surface Integrals & Vector Theorems")

    # 8.1 Parameterized surface with normal vectors
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Parameterized Surface with Normal Vectors\n$\\mathbf{N} = \\mathbf{r}_u \\times \\mathbf{r}_v$', fontsize=13)
    u = np.linspace(0, 2*np.pi, 30); v = np.linspace(-1, 1, 15)
    U, V = np.meshgrid(u, v)
    R = 2
    X = (R + V*np.cos(U/2))*np.cos(U)
    Y = (R + V*np.cos(U/2))*np.sin(U)
    Z = V*np.sin(U/2)
    ax.plot_surface(X, Y, Z, alpha=0.5, cmap='Blues_r')
    # Normal vectors at sample points
    for ui in np.linspace(0, 2*np.pi, 12):
        for vi in np.linspace(-0.8, 0.8, 3):
            px = (R + vi*np.cos(ui/2))*np.cos(ui)
            py = (R + vi*np.cos(ui/2))*np.sin(ui)
            pz = vi*np.sin(ui/2)
            nx = np.cos(ui)*np.cos(ui/2)
            ny = np.sin(ui)*np.cos(ui/2)
            nz = np.sin(ui/2)
            nrm = np.sqrt(nx**2+ny**2+nz**2)
            ax.quiver(px, py, pz, nx/nrm*0.3, ny/nrm*0.3, nz/nrm*0.3,
                      color='red', linewidth=1.5, arrow_length_ratio=0.3, alpha=0.8)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    save(fig, '08-surface-normals.png')

    # 8.2 Stokes's Theorem visualization
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Stokes's Theorem: $\\oint_C \\mathbf{F}\\cdot d\\mathbf{r} = \\iint_S (\\nabla\\times\\mathbf{F})\\cdot d\\mathbf{S}$",
                 fontsize=13)
    # A surface (paraboloid cap)
    r_disk = np.linspace(0, 1.5, 15); theta = np.linspace(0, 2*np.pi, 30)
    R, T = np.meshgrid(r_disk, theta)
    X = R*np.cos(T); Y = R*np.sin(T); Z = 2 - (X**2 + Y**2)
    ax.plot_surface(X, Y, Z, alpha=0.5, cmap='Blues_r')
    # Boundary curve C: circle at z=2-2.25 = -0.25 ... wait let me use z=1
    # Actually let me use: surface z = 1 - x^2 - y^2, boundary at z=0: x^2+y^2=1
    x_surf = np.linspace(-1, 1, 30); y_surf = np.linspace(-1, 1, 30)
    Xs, Ys = np.meshgrid(x_surf, y_surf)
    Zs = 1 - Xs**2 - Ys**2
    mask = Xs**2 + Ys**2 <= 1
    Zs[~mask] = np.nan
    ax.plot_surface(Xs, Ys, Zs, alpha=0.5, cmap='Blues_r')

    # Boundary C
    t = np.linspace(0, 2*np.pi, 100)
    bx, by, bz = np.cos(t), np.sin(t), np.zeros_like(t)
    ax.plot(bx, by, bz, 'r-', linewidth=3, label='Boundary $C$')

    # Curl vectors on surface
    for xi in np.linspace(-0.6, 0.6, 5):
        for yi in np.linspace(-0.6, 0.6, 5):
            if xi**2 + yi**2 < 0.9:
                zi = 1 - xi**2 - yi**2
                ax.quiver(xi, yi, zi, 0, 0, 0.15, color='green', linewidth=1.5,
                          arrow_length_ratio=0.3, alpha=0.6)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.legend(fontsize=10)
    save(fig, '08-stokes-theorem.png')

    # 8.3 Divergence Theorem visualization
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Divergence Theorem: $\\iint_{\\partial V} \\mathbf{F}\\cdot d\\mathbf{S} = \\iiint_V \\nabla\\cdot\\mathbf{F}\\,dV$",
                 fontsize=13)
    # A sphere
    u_sph = np.linspace(0, 2*np.pi, 30); v_sph = np.linspace(0, np.pi, 20)
    U, V = np.meshgrid(u_sph, v_sph)
    R = 1.5
    X = R*np.sin(V)*np.cos(U); Y = R*np.sin(V)*np.sin(U); Z = R*np.cos(V)
    ax.plot_surface(X, Y, Z, alpha=0.3, color='blue')
    # Flux vectors on surface
    for ui in np.linspace(0, 2*np.pi, 16):
        for vi in np.linspace(np.pi/6, 5*np.pi/6, 5):
            sx = R*np.sin(vi)*np.cos(ui)
            sy = R*np.sin(vi)*np.sin(ui)
            sz = R*np.cos(vi)
            # Outward normal = position vector for sphere
            nrm = R
            ax.quiver(sx, sy, sz, sx/nrm*0.4, sy/nrm*0.4, sz/nrm*0.4,
                      color='red', linewidth=1.5, arrow_length_ratio=0.25, alpha=0.7)
    # Divergence sources inside (density)
    interior_pts = np.random.uniform(-0.8, 0.8, (30, 3))
    interior_pts = interior_pts[np.sum(interior_pts**2, axis=1) < R**2]
    ax.scatter(interior_pts[:,0], interior_pts[:,1], interior_pts[:,2],
               c='orange', s=15, alpha=0.6, label='Sources ($\\nabla\\cdot\\mathbf{F}>0$)')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.legend(fontsize=10)
    save(fig, '08-divergence-theorem.png')

    # 8.4 Vector calculus summary: all three theorems
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    titles = [
        "Green's Theorem (2D)\n$\\oint\\mathbf{F}\\cdot d\\mathbf{r}=\\iint(\\nabla\\times\\mathbf{F})\\cdot\\mathbf{k}\\,dA$",
        "Stokes's Theorem (3D)\n$\\oint\\mathbf{F}\\cdot d\\mathbf{r}=\\iint(\\nabla\\times\\mathbf{F})\\cdot\\mathbf{n}\\,dS$",
        "Divergence Theorem (3D)\n$\\iint\\mathbf{F}\\cdot\\mathbf{n}\\,dS=\\iiint\\nabla\\cdot\\mathbf{F}\\,dV$",
    ]
    for ax, title in zip(axes, titles):
        ax.set_title(title, fontsize=10)
        ax.set_aspect('equal')
        ax.set_xlim(-2,2); ax.set_ylim(-2,2)
        ax.axis('off')

    # Left: Green - planar region with circulation on boundary
    theta = np.linspace(0, 2*np.pi, 200)
    axes[0].fill(1.5*np.cos(theta), np.sin(theta), alpha=0.2, color='blue')
    axes[0].plot(1.5*np.cos(theta), np.sin(theta), 'b-', linewidth=2.5)
    for t0 in np.linspace(0, 2*np.pi, 12):
        axes[0].quiver(1.5*np.cos(t0), np.sin(t0), -0.3*np.sin(t0), 0.3*np.cos(t0),
                       angles='xy', scale_units='xy', scale=0.8, color='red', width=0.03)
    for xi, yi in [(0,0),(0.5,0.5),(-0.5,-0.3),(0.3,-0.5)]:
        axes[0].quiver(xi, yi, -0.2*yi, 0.2*xi, angles='xy', scale_units='xy', scale=1,
                       color='green', alpha=0.5, width=0.02)

    # Middle: Stokes - surface with boundary
    t = np.linspace(0, 2*np.pi, 200)
    axes[1].fill(np.cos(t), np.sin(t), alpha=0.3, color='blue')
    for xi in np.linspace(-0.5, 0.5, 5):
        for yi in np.linspace(-0.5, 0.5, 5):
            if xi**2+yi**2 < 0.8:
                axes[1].quiver(xi, yi, -0.1*yi, 0.1*xi, angles='xy', scale_units='xy', scale=1,
                               color='green', alpha=0.6, width=0.02)

    # Right: Divergence - volume with flux on boundary
    axes[2].fill(np.cos(theta), np.sin(theta), alpha=0.2, color='blue')
    axes[2].plot(np.cos(theta), np.sin(theta), 'b-', linewidth=2.5)
    for t0 in np.linspace(0, 2*np.pi, 12):
        axes[2].quiver(np.cos(t0), np.sin(t0), 0.2*np.cos(t0), 0.2*np.sin(t0),
                       angles='xy', scale_units='xy', scale=0.8, color='red', width=0.03)
    axes[2].scatter([0,0.3,-0.3,0.5,-0.4], [0,0.2,-0.4,-0.1,0.3], c='orange', s=30, alpha=0.6)

    fig.suptitle('The Three Great Theorems of Vector Calculus', fontsize=15, y=1.02)
    save(fig, '08-three-theorems.png')


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    print(f"Saving images to: {OUT}")
    blog1_images()
    blog2_images()
    blog3_images()
    blog4_images()
    blog5_images()
    blog6_images()
    blog7_images()
    blog8_images()
    print(f"\nDone! All images saved to {OUT}")
