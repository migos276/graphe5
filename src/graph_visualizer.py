"""
Module de visualisation pour les graphes et leur k-connexité
Utilise matplotlib et networkx pour créer des visualisations interactives
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import numpy as np
from typing import Dict, List, Set, Tuple, Optional
import colorsys

class GraphVisualizer:
    """
    Classe pour visualiser les graphes et leur analyse de k-connexité
    """
    
    def __init__(self):
        """
        Initialise le visualiseur
        """
        self.fig = None
        self.ax = None
        self.pos = None
        
        # Configuration des couleurs
        self.color_scheme = {
            'node_default': '#4A90E2',
            'node_cut': '#E74C3C',
            'node_highlight': '#F39C12',
            'edge_default': '#7F8C8D',
            'edge_cut': '#E74C3C',
            'edge_highlight': '#F39C12',
            'background': '#FFFFFF'
        }
    
    def setup_plot(self, figsize: Tuple[int, int] = (12, 8)) -> None:
        """
        Configure la figure matplotlib
        
        Args:
            figsize: Taille de la figure (largeur, hauteur)
        """
        plt.style.use('default')
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.fig.patch.set_facecolor(self.color_scheme['background'])
        self.ax.set_facecolor(self.color_scheme['background'])
        
        # Configuration des axes
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # Titre personnalisé
        self.ax.set_title('Analyse de K-Connexité', 
                         fontsize=16, fontweight='bold', pad=20)
    
    def calculate_layout(self, graph: nx.Graph, layout_type: str = 'spring') -> Dict:
        """
        Calcule la disposition des nœuds
        
        Args:
            graph: Graphe NetworkX
            layout_type: Type de layout ('spring', 'circular', 'random', 'shell')
        
        Returns:
            Dict: Positions des nœuds
        """
        if layout_type == 'spring':
            self.pos = nx.spring_layout(graph, k=3, iterations=50, seed=42)
        elif layout_type == 'circular':
            self.pos = nx.circular_layout(graph)
        elif layout_type == 'random':
            self.pos = nx.random_layout(graph, seed=42)
        elif layout_type == 'shell':
            self.pos = nx.shell_layout(graph)
        else:
            # Layout par défaut
            self.pos = nx.spring_layout(graph, k=3, iterations=50, seed=42)
        
        return self.pos
    
    def draw_graph_basic(self, graph: nx.Graph, layout_type: str = 'spring') -> None:
        """
        Dessine le graphe de base
        
        Args:
            graph: Graphe NetworkX
            layout_type: Type de layout
        """
        if not self.fig:
            self.setup_plot()
        
        # Calcul de la disposition
        self.calculate_layout(graph, layout_type)
        
        # Dessin des arêtes
        nx.draw_networkx_edges(graph, self.pos,
                              edge_color=self.color_scheme['edge_default'],
                              width=1.5, alpha=0.6, ax=self.ax)
        
        # Dessin des nœuds
        nx.draw_networkx_nodes(graph, self.pos,
                              node_color=self.color_scheme['node_default'],
                              node_size=500, alpha=0.8, ax=self.ax)
        
        # Étiquettes des nœuds
        nx.draw_networkx_labels(graph, self.pos,
                               font_size=10, font_weight='bold',
                               font_color='white', ax=self.ax)
        
        # Informations sur le graphe
        info_text = f"Nœuds: {graph.number_of_nodes()} | Arêtes: {graph.number_of_edges()}\n"
        info_text += f"Connexe: {'Oui' if nx.is_connected(graph) else 'Non'}"
        
        self.ax.text(0.02, 0.98, info_text, transform=self.ax.transAxes,
                    fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    def draw_connectivity_analysis(self, graph: nx.Graph, results: Dict, 
                                  layout_type: str = 'spring') -> None:
        """
        Dessine le graphe avec l'analyse de connexité
        
        Args:
            graph: Graphe NetworkX
            results: Résultats de l'analyse de connexité
            layout_type: Type de layout
        """
        if not self.fig:
            self.setup_plot()
        
        # Calcul de la disposition
        self.calculate_layout(graph, layout_type)
        
        # Récupération des coupes
        node_cut = set(results['cuts']['minimum_node_cut'])
        edge_cut = set(results['cuts']['minimum_edge_cut'])
        
        # Couleurs des nœuds
        node_colors = []
        for node in graph.nodes():
            if node in node_cut:
                node_colors.append(self.color_scheme['node_cut'])
            else:
                node_colors.append(self.color_scheme['node_default'])
        
        # Couleurs des arêtes
        edge_colors = []
        for edge in graph.edges():
            if edge in edge_cut or (edge[1], edge[0]) in edge_cut:
                edge_colors.append(self.color_scheme['edge_cut'])
            else:
                edge_colors.append(self.color_scheme['edge_default'])
        
        # Dessin des arêtes
        nx.draw_networkx_edges(graph, self.pos,
                              edge_color=edge_colors,
                              width=2, alpha=0.7, ax=self.ax)
        
        # Dessin des nœuds
        nx.draw_networkx_nodes(graph, self.pos,
                              node_color=node_colors,
                              node_size=600, alpha=0.9, ax=self.ax)
        
        # Étiquettes des nœuds
        nx.draw_networkx_labels(graph, self.pos,
                               font_size=10, font_weight='bold',
                               font_color='white', ax=self.ax)
        
        # Légende
        self._add_connectivity_legend(results)
        
        # Titre spécialisé
        node_conn = results['connectivity']['node_connectivity']
        edge_conn = results['connectivity']['edge_connectivity']
        self.ax.set_title(f'Analyse K-Connexité | κ(G)={node_conn}, λ(G)={edge_conn}',
                         fontsize=16, fontweight='bold', pad=20)
    
    def _add_connectivity_legend(self, results: Dict) -> None:
        """
        Ajoute une légende pour l'analyse de connexité
        
        Args:
            results: Résultats de l'analyse
        """
        # Informations principales
        info_text = f"Connexité par nœuds: κ(G) = {results['connectivity']['node_connectivity']}\n"
        info_text += f"Connexité par arêtes: λ(G) = {results['connectivity']['edge_connectivity']}\n\n"
        
        # Coupes minimales
        if results['cuts']['minimum_node_cut']:
            info_text += f"Coupe de nœuds: {results['cuts']['minimum_node_cut']}\n"
        if results['cuts']['minimum_edge_cut']:
            info_text += f"Coupe d'arêtes: {len(results['cuts']['minimum_edge_cut'])} arête(s)\n"
        
        # Positionnement de la légende
        self.ax.text(0.02, 0.02, info_text, transform=self.ax.transAxes,
                    fontsize=9, verticalalignment='bottom',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        # Légende des couleurs
        legend_elements = []
        if results['cuts']['minimum_node_cut']:
            legend_elements.append(patches.Patch(color=self.color_scheme['node_cut'], 
                                               label='Nœuds de coupe'))
        if results['cuts']['minimum_edge_cut']:
            legend_elements.append(patches.Patch(color=self.color_scheme['edge_cut'], 
                                               label='Arêtes de coupe'))
        
        if legend_elements:
            self.ax.legend(handles=legend_elements, loc='upper right', 
                          bbox_to_anchor=(0.98, 0.98))
    
    def draw_k_connectivity_comparison(self, graph: nx.Graph, results: Dict, 
                                     max_k: int = 5) -> None:
        """
        Dessine une comparaison visuelle pour différentes valeurs de k
        
        Args:
            graph: Graphe NetworkX
            results: Résultats de l'analyse
            max_k: Valeur maximale de k à afficher
        """
        # Configuration de la figure avec sous-graphiques
        fig, axes = plt.subplots(2, min(max_k, 3), figsize=(15, 10))
        if max_k == 1:
            axes = [axes]
        elif max_k <= 3:
            axes = axes.flatten()
        
        fig.suptitle('Comparaison K-Connexité', fontsize=16, fontweight='bold')
        
        # Calcul de la disposition commune
        pos = nx.spring_layout(graph, k=3, iterations=50, seed=42)
        
        node_conn = results['connectivity']['node_connectivity']
        edge_conn = results['connectivity']['edge_connectivity']
        
        for i, k in enumerate(range(1, min(max_k + 1, len(axes) + 1))):
            if i >= len(axes):
                break
                
            ax = axes[i] if hasattr(axes, '__len__') else axes
            
            # Couleurs selon la k-connexité
            node_colors = []
            edge_colors = []
            
            k_node_connected = k <= node_conn
            k_edge_connected = k <= edge_conn
            
            # Nœuds
            for node in graph.nodes():
                if k_node_connected:
                    node_colors.append('#2ECC71')  # Vert pour connexe
                else:
                    node_colors.append('#E74C3C')  # Rouge pour non-connexe
            
            # Arêtes
            for edge in graph.edges():
                if k_edge_connected:
                    edge_colors.append('#27AE60')  # Vert foncé pour connexe
                else:
                    edge_colors.append('#C0392B')  # Rouge foncé pour non-connexe
            
            # Dessin
            nx.draw_networkx_edges(graph, pos, edge_color=edge_colors,
                                  width=1.5, alpha=0.7, ax=ax)
            nx.draw_networkx_nodes(graph, pos, node_color=node_colors,
                                  node_size=300, alpha=0.8, ax=ax)
            nx.draw_networkx_labels(graph, pos, font_size=8, 
                                   font_color='white', ax=ax)
            
            # Titre et informations
            status_node = "✓" if k_node_connected else "✗"
            status_edge = "✓" if k_edge_connected else "✗"
            
            ax.set_title(f'k = {k}\nNœuds: {status_node} | Arêtes: {status_edge}',
                        fontsize=10, fontweight='bold')
            ax.axis('off')
        
        # Masquer les axes inutilisés
        for i in range(min(max_k, len(axes)), len(axes)):
            if hasattr(axes, '__len__') and i < len(axes):
                axes[i].axis('off')
        
        plt.tight_layout()
        self.fig = fig
    
    def save_visualization(self, filepath: str, dpi: int = 300) -> bool:
        """
        Sauvegarde la visualisation
        
        Args:
            filepath: Chemin de sauvegarde
            dpi: Résolution de l'image
        
        Returns:
            bool: True si la sauvegarde réussit
        """
        try:
            if self.fig:
                self.fig.savefig(filepath, dpi=dpi, bbox_inches='tight', 
                               facecolor=self.color_scheme['background'])
                print(f"✓ Visualisation sauvegardée: {filepath}")
                return True
            else:
                print("✗ Aucune visualisation à sauvegarder")
                return False
        except Exception as e:
            print(f"✗ Erreur lors de la sauvegarde: {e}")
            return False
    
    def show(self) -> None:
        """
        Affiche la visualisation
        """
        if self.fig:
            plt.show()
        else:
            print("✗ Aucune visualisation à afficher")
    
    def clear(self) -> None:
        """
        Efface la visualisation actuelle
        """
        if self.fig:
            plt.close(self.fig)
        self.fig = None
        self.ax = None
        self.pos = None
