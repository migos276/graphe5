"""
Module principal pour le calcul de la k-connexité des graphes
Supporte tous types de graphes (orientés/non-orientés, avec boucles)
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from itertools import combinations
import copy

class GraphConnectivityAnalyzer:
    """
    Classe principale pour analyser la k-connexité des graphes
    """
    
    def __init__(self, graph: nx.Graph = None):
        """
        Initialise l'analyseur avec un graphe optionnel
        
        Args:
            graph: Graphe NetworkX (optionnel)
        """
        self.graph = graph
        self.connectivity_results = {}
        self.analysis_cache = {}
    
    def load_graph_from_file(self, filepath: str, format_type: str = 'edgelist') -> bool:
        """
        Charge un graphe depuis un fichier
        
        Args:
            filepath: Chemin vers le fichier
            format_type: Format du fichier ('edgelist', 'gml', 'graphml', 'adjlist')
        
        Returns:
            bool: True si le chargement réussit
        """
        try:
            if format_type == 'edgelist':
                self.graph = nx.read_edgelist(filepath, create_using=nx.Graph())
            elif format_type == 'gml':
                self.graph = nx.read_gml(filepath)
            elif format_type == 'graphml':
                self.graph = nx.read_graphml(filepath)
            elif format_type == 'adjlist':
                self.graph = nx.read_adjlist(filepath)
            else:
                raise ValueError(f"Format non supporté: {format_type}")
            
            # Gestion des boucles et arêtes multiples
            if isinstance(self.graph, nx.MultiGraph):
                self.graph = nx.Graph(self.graph)  # Conversion en graphe simple
            
            print(f"✓ Graphe chargé: {self.graph.number_of_nodes()} nœuds, {self.graph.number_of_edges()} arêtes")
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors du chargement: {e}")
            return False
    
    def create_graph_from_edges(self, edges: List[Tuple], directed: bool = False) -> bool:
        """
        Crée un graphe à partir d'une liste d'arêtes
        
        Args:
            edges: Liste de tuples (u, v) représentant les arêtes
            directed: True pour un graphe orienté
        
        Returns:
            bool: True si la création réussit
        """
        try:
            if directed:
                self.graph = nx.DiGraph()
            else:
                self.graph = nx.Graph()
            
            self.graph.add_edges_from(edges)
            
            print(f"✓ Graphe créé: {self.graph.number_of_nodes()} nœuds, {self.graph.number_of_edges()} arêtes")
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors de la création: {e}")
            return False
    
    def node_connectivity(self) -> int:
        """
        Calcule la connexité par nœuds (κ(G))
        
        Returns:
            int: Connexité par nœuds
        """
        if not self.graph:
            return 0
        
        if 'node_connectivity' in self.analysis_cache:
            return self.analysis_cache['node_connectivity']
        
        try:
            # Cas spéciaux
            if self.graph.number_of_nodes() <= 1:
                connectivity = 0
            elif not nx.is_connected(self.graph):
                connectivity = 0
            elif nx.is_complete_graph(self.graph):
                connectivity = self.graph.number_of_nodes() - 1
            else:
                # Calcul général utilisant l'algorithme de flux maximal
                connectivity = nx.node_connectivity(self.graph)
            
            self.analysis_cache['node_connectivity'] = connectivity
            return connectivity
            
        except Exception as e:
            print(f"Erreur lors du calcul de la connexité par nœuds: {e}")
            return 0
    
    def edge_connectivity(self) -> int:
        """
        Calcule la connexité par arêtes (λ(G))
        
        Returns:
            int: Connexité par arêtes
        """
        if not self.graph:
            return 0
        
        if 'edge_connectivity' in self.analysis_cache:
            return self.analysis_cache['edge_connectivity']
        
        try:
            # Cas spéciaux
            if self.graph.number_of_nodes() <= 1:
                connectivity = 0
            elif not nx.is_connected(self.graph):
                connectivity = 0
            else:
                # Calcul utilisant l'algorithme de flux maximal
                connectivity = nx.edge_connectivity(self.graph)
            
            self.analysis_cache['edge_connectivity'] = connectivity
            return connectivity
            
        except Exception as e:
            print(f"Erreur lors du calcul de la connexité par arêtes: {e}")
            return 0
    
    def minimum_node_cut(self) -> Set:
        """
        Trouve un ensemble minimal de nœuds dont la suppression déconnecte le graphe
        
        Returns:
            Set: Ensemble des nœuds de la coupe minimale
        """
        if not self.graph or not nx.is_connected(self.graph):
            return set()
        
        try:
            if nx.is_complete_graph(self.graph):
                # Pour un graphe complet, on peut retirer n'importe quels n-1 nœuds
                nodes = list(self.graph.nodes())
                return set(nodes[:-1])
            
            return nx.minimum_node_cut(self.graph)
            
        except Exception as e:
            print(f"Erreur lors du calcul de la coupe minimale: {e}")
            return set()
    
    def minimum_edge_cut(self) -> Set:
        """
        Trouve un ensemble minimal d'arêtes dont la suppression déconnecte le graphe
        
        Returns:
            Set: Ensemble des arêtes de la coupe minimale
        """
        if not self.graph or not nx.is_connected(self.graph):
            return set()
        
        try:
            return nx.minimum_edge_cut(self.graph)
            
        except Exception as e:
            print(f"Erreur lors du calcul de la coupe d'arêtes minimale: {e}")
            return set()
    
    def k_connectivity_analysis(self, max_k: int = None) -> Dict:
        """
        Analyse complète de la k-connexité
        
        Args:
            max_k: Valeur maximale de k à tester (par défaut: nombre de nœuds)
        
        Returns:
            Dict: Résultats de l'analyse
        """
        if not self.graph:
            return {}
        
        n_nodes = self.graph.number_of_nodes()
        if max_k is None:
            max_k = n_nodes
        
        results = {
            'basic_info': {
                'nodes': n_nodes,
                'edges': self.graph.number_of_edges(),
                'is_connected': nx.is_connected(self.graph),
                'is_directed': self.graph.is_directed()
            },
            'connectivity': {
                'node_connectivity': self.node_connectivity(),
                'edge_connectivity': self.edge_connectivity()
            },
            'cuts': {
                'minimum_node_cut': list(self.minimum_node_cut()),
                'minimum_edge_cut': list(self.minimum_edge_cut())
            },
            'k_analysis': {}
        }
        
        # Analyse pour différentes valeurs de k
        node_conn = results['connectivity']['node_connectivity']
        edge_conn = results['connectivity']['edge_connectivity']
        
        for k in range(1, min(max_k + 1, n_nodes)):
            results['k_analysis'][k] = {
                'k_node_connected': k <= node_conn,
                'k_edge_connected': k <= edge_conn,
                'description': self._get_k_connectivity_description(k, node_conn, edge_conn)
            }
        
        self.connectivity_results = results
        return results
    
    def _get_k_connectivity_description(self, k: int, node_conn: int, edge_conn: int) -> str:
        """
        Génère une description de la k-connexité
        
        Args:
            k: Valeur de k
            node_conn: Connexité par nœuds
            edge_conn: Connexité par arêtes
        
        Returns:
            str: Description textuelle
        """
        descriptions = []
        
        if k <= node_conn:
            descriptions.append(f"Le graphe est {k}-connexe par nœuds")
        else:
            descriptions.append(f"Le graphe N'EST PAS {k}-connexe par nœuds")
        
        if k <= edge_conn:
            descriptions.append(f"Le graphe est {k}-connexe par arêtes")
        else:
            descriptions.append(f"Le graphe N'EST PAS {k}-connexe par arêtes")
        
        return " | ".join(descriptions)
    
    def get_summary(self) -> str:
        """
        Génère un résumé de l'analyse de connexité
        
        Returns:
            str: Résumé formaté
        """
        if not self.connectivity_results:
            self.k_connectivity_analysis()
        
        results = self.connectivity_results
        
        summary = f"""
═══════════════════════════════════════════════════════════════
                    ANALYSE DE K-CONNEXITÉ
═══════════════════════════════════════════════════════════════

📊 INFORMATIONS GÉNÉRALES:
   • Nombre de nœuds: {results['basic_info']['nodes']}
   • Nombre d'arêtes: {results['basic_info']['edges']}
   • Graphe connexe: {'✓ Oui' if results['basic_info']['is_connected'] else '✗ Non'}
   • Graphe orienté: {'✓ Oui' if results['basic_info']['is_directed'] else '✗ Non'}

🔗 CONNEXITÉ:
   • Connexité par nœuds κ(G): {results['connectivity']['node_connectivity']}
   • Connexité par arêtes λ(G): {results['connectivity']['edge_connectivity']}

✂️ COUPES MINIMALES:
   • Coupe de nœuds: {results['cuts']['minimum_node_cut']}
   • Coupe d'arêtes: {results['cuts']['minimum_edge_cut']}

📈 ANALYSE K-CONNEXITÉ:"""
        
        for k, analysis in results['k_analysis'].items():
            summary += f"\n   • k={k}: {analysis['description']}"
        
        summary += "\n═══════════════════════════════════════════════════════════════"
        
        return summary
    
    def export_results(self, filepath: str, format_type: str = 'json') -> bool:
        """
        Exporte les résultats de l'analyse
        
        Args:
            filepath: Chemin de sauvegarde
            format_type: Format d'export ('json', 'txt')
        
        Returns:
            bool: True si l'export réussit
        """
        try:
            if format_type == 'json':
                import json
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.connectivity_results, f, indent=2, ensure_ascii=False)
            elif format_type == 'txt':
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.get_summary())
            else:
                raise ValueError(f"Format non supporté: {format_type}")
            
            print(f"✓ Résultats exportés vers: {filepath}")
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors de l'export: {e}")
            return False
