"""
Interface utilisateur principale pour l'analyse de k-connexité des graphes
Programme modulaire avec interface fluide et intuitive
"""

import os
import sys
from typing import List, Tuple, Optional
import networkx as nx

# Import des modules locaux
from graph_connectivity import GraphConnectivityAnalyzer
from graph_visualizer import GraphVisualizer

class GraphConnectivityInterface:
    """
    Interface utilisateur principale pour l'analyse de k-connexité
    """
    
    def __init__(self):
        """
        Initialise l'interface
        """
        self.analyzer = GraphConnectivityAnalyzer()
        self.visualizer = GraphVisualizer()
        self.current_graph = None
        self.current_results = None
        
        # Configuration
        self.supported_formats = ['edgelist', 'gml', 'graphml', 'adjlist']
        self.example_graphs = self._create_example_graphs()
    
    def _create_example_graphs(self) -> dict:
        """
        Crée des graphes d'exemple pour les démonstrations
        
        Returns:
            dict: Dictionnaire des graphes d'exemple
        """
        examples = {}
        
        # Graphe complet K4
        examples['K4'] = nx.complete_graph(4)
        
        # Cycle C5
        examples['C5'] = nx.cycle_graph(5)
        
        # Graphe en étoile
        examples['star'] = nx.star_graph(5)
        
        # Graphe de Petersen
        examples['petersen'] = nx.petersen_graph()
        
        # Graphe avec pont
        bridge_graph = nx.Graph()
        bridge_graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 1), (2, 5), (5, 6), (6, 7), (7, 8), (8, 5)])
        examples['bridge'] = bridge_graph
        
        # Graphe non connexe
        disconnected = nx.Graph()
        disconnected.add_edges_from([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5)])
        examples['disconnected'] = disconnected
        
        return examples
    
    def display_welcome(self) -> None:
        """
        Affiche le message d'accueil et le guide
        """
        welcome_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ANALYSEUR DE K-CONNEXITÉ                           ║
║                     Analyse complète des graphes NetworkX                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 FONCTIONNALITÉS:
   • Calcul de la connexité par nœuds κ(G) et par arêtes λ(G)
   • Détection des coupes minimales
   • Analyse k-connexité pour différentes valeurs de k
   • Visualisation interactive avec matplotlib
   • Support de tous types de graphes (orientés, avec boucles, etc.)
   • Export des résultats (JSON, TXT)

📚 GUIDE D'UTILISATION:
   1. Chargez un graphe (fichier ou création manuelle)
   2. Lancez l'analyse de k-connexité
   3. Visualisez les résultats
   4. Exportez si nécessaire

🔧 FORMATS SUPPORTÉS:
   • EdgeList (.txt)
   • GML (.gml)
   • GraphML (.graphml)
   • AdjacencyList (.adjlist)

📊 EXEMPLES DISPONIBLES:
   • K4: Graphe complet à 4 nœuds
   • C5: Cycle à 5 nœuds
   • Star: Graphe en étoile
   • Petersen: Graphe de Petersen
   • Bridge: Graphe avec pont
   • Disconnected: Graphe non connexe

═══════════════════════════════════════════════════════════════════════════════
"""
        print(welcome_text)
    
    def display_menu(self) -> None:
        """
        Affiche le menu principal
        """
        menu_text = """
┌─────────────────── MENU PRINCIPAL ───────────────────┐
│                                                      │
│  1. 📁 Charger un graphe depuis un fichier          │
│  2. ✏️  Créer un graphe manuellement                 │
│  3. 🎲 Utiliser un graphe d'exemple                 │
│  4. 📊 Analyser la k-connexité                      │
│  5. 📈 Visualiser le graphe                         │
│  6. 🔍 Visualiser l'analyse de connexité            │
│  7. 📉 Comparaison k-connexité                      │
│  8. 💾 Exporter les résultats                       │
│  9. ℹ️  Informations sur le graphe actuel           │
│  10. 🆘 Aide détaillée                              │
│  0. 🚪 Quitter                                       │
│                                                      │
└──────────────────────────────────────────────────────┘
        """
        print(menu_text)
    
    def load_graph_from_file(self) -> bool:
        """
        Interface pour charger un graphe depuis un fichier
        
        Returns:
            bool: True si le chargement réussit
        """
        print("\n" + "="*60)
        print("         CHARGEMENT D'UN GRAPHE DEPUIS UN FICHIER")
        print("="*60)
        
        # Demande du chemin du fichier
        filepath = input("\n📁 Chemin vers le fichier: ").strip()
        
        if not os.path.exists(filepath):
            print(f"❌ Fichier non trouvé: {filepath}")
            return False
        
        # Détection automatique du format ou demande à l'utilisateur
        print(f"\n🔍 Formats supportés: {', '.join(self.supported_formats)}")
        format_choice = input("📋 Format du fichier (auto-détection si vide): ").strip().lower()
        
        if not format_choice:
            # Auto-détection basée sur l'extension
            ext = os.path.splitext(filepath)[1].lower()
            format_mapping = {
                '.txt': 'edgelist',
                '.edgelist': 'edgelist',
                '.gml': 'gml',
                '.graphml': 'graphml',
                '.adjlist': 'adjlist'
            }
            format_choice = format_mapping.get(ext, 'edgelist')
            print(f"🤖 Format détecté: {format_choice}")
        
        # Chargement
        success = self.analyzer.load_graph_from_file(filepath, format_choice)
        
        if success:
            self.current_graph = self.analyzer.graph
            print(f"✅ Graphe chargé avec succès!")
            self._display_graph_info()
        
        return success
    
    def create_graph_manually(self) -> bool:
        """
        Interface pour créer un graphe manuellement
        
        Returns:
            bool: True si la création réussit
        """
        print("\n" + "="*60)
        print("           CRÉATION MANUELLE D'UN GRAPHE")
        print("="*60)
        
        # Type de graphe
        print("\n🔧 Types de graphe:")
        print("   1. Non orienté (par défaut)")
        print("   2. Orienté")
        
        graph_type = input("\n📋 Choisissez le type (1 ou 2): ").strip()
        directed = (graph_type == '2')
        
        print(f"\n📝 Saisie des arêtes pour un graphe {'orienté' if directed else 'non orienté'}")
        print("   Format: nœud1 nœud2 (exemple: A B)")
        print("   Tapez 'fin' pour terminer")
        
        edges = []
        while True:
            edge_input = input(f"\n🔗 Arête {len(edges) + 1}: ").strip()
            
            if edge_input.lower() == 'fin':
                break
            
            try:
                parts = edge_input.split()
                if len(parts) != 2:
                    print("❌ Format incorrect. Utilisez: nœud1 nœud2")
                    continue
                
                # Conversion en entier si possible, sinon garde comme string
                try:
                    node1 = int(parts[0])
                    node2 = int(parts[1])
                except ValueError:
                    node1 = parts[0]
                    node2 = parts[1]
                
                edges.append((node1, node2))
                print(f"✅ Arête ajoutée: {node1} -- {node2}")
                
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        if not edges:
            print("❌ Aucune arête saisie.")
            return False
        
        # Création du graphe
        success = self.analyzer.create_graph_from_edges(edges, directed)
        
        if success:
            self.current_graph = self.analyzer.graph
            print(f"✅ Graphe créé avec succès!")
            self._display_graph_info()
        
        return success
    
    def use_example_graph(self) -> bool:
        """
        Interface pour utiliser un graphe d'exemple
        
        Returns:
            bool: True si la sélection réussit
        """
        print("\n" + "="*60)
        print("              GRAPHES D'EXEMPLE")
        print("="*60)
        
        print("\n📚 Graphes disponibles:")
        examples_list = list(self.example_graphs.keys())
        
        for i, (name, graph) in enumerate(self.example_graphs.items(), 1):
            n_nodes = graph.number_of_nodes()
            n_edges = graph.number_of_edges()
            connected = "Connexe" if nx.is_connected(graph) else "Non connexe"
            print(f"   {i}. {name}: {n_nodes} nœuds, {n_edges} arêtes ({connected})")
        
        try:
            choice = int(input(f"\n🎯 Choisissez un graphe (1-{len(examples_list)}): "))
            
            if 1 <= choice <= len(examples_list):
                selected_name = examples_list[choice - 1]
                selected_graph = self.example_graphs[selected_name].copy()
                
                # Configuration de l'analyseur
                self.analyzer.graph = selected_graph
                self.current_graph = selected_graph
                
                print(f"✅ Graphe '{selected_name}' sélectionné!")
                self._display_graph_info()
                return True
            else:
                print("❌ Choix invalide.")
                return False
                
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
            return False
    
    def analyze_connectivity(self) -> bool:
        """
        Lance l'analyse de k-connexité
        
        Returns:
            bool: True si l'analyse réussit
        """
        if not self.current_graph:
            print("❌ Aucun graphe chargé. Veuillez d'abord charger un graphe.")
            return False
        
        print("\n" + "="*60)
        print("           ANALYSE DE K-CONNEXITÉ")
        print("="*60)
        
        # Options d'analyse
        max_k = self.current_graph.number_of_nodes()
        print(f"\n🔧 Valeur maximale de k recommandée: {max_k}")
        
        user_max_k = input(f"📊 Valeur maximale de k à analyser (défaut: {max_k}): ").strip()
        
        if user_max_k:
            try:
                max_k = int(user_max_k)
            except ValueError:
                print("⚠️ Valeur invalide, utilisation de la valeur par défaut.")
        
        # Lancement de l'analyse
        print("\n🔄 Analyse en cours...")
        
        try:
            self.current_results = self.analyzer.k_connectivity_analysis(max_k)
            
            if self.current_results:
                print("✅ Analyse terminée!")
                print("\n" + self.analyzer.get_summary())
                return True
            else:
                print("❌ Erreur lors de l'analyse.")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            return False
    
    def visualize_graph(self) -> None:
        """
        Visualise le graphe de base
        """
        if not self.current_graph:
            print("❌ Aucun graphe chargé. Veuillez d'abord charger un graphe.")
            return
        
        print("\n🎨 Génération de la visualisation...")
        
        # Options de layout
        layouts = ['spring', 'circular', 'random', 'shell']
        print(f"📐 Layouts disponibles: {', '.join(layouts)}")
        layout_choice = input("🎯 Layout (défaut: spring): ").strip().lower()
        
        if layout_choice not in layouts:
            layout_choice = 'spring'
        
        try:
            self.visualizer.clear()
            self.visualizer.draw_graph_basic(self.current_graph, layout_choice)
            self.visualizer.show()
            
        except Exception as e:
            print(f"❌ Erreur lors de la visualisation: {e}")
    
    def visualize_connectivity(self) -> None:
        """
        Visualise l'analyse de connexité
        """
        if not self.current_graph:
            print("❌ Aucun graphe chargé.")
            return
        
        if not self.current_results:
            print("⚠️ Aucune analyse disponible. Lancement de l'analyse...")
            if not self.analyze_connectivity():
                return
        
        print("\n🎨 Génération de la visualisation de connexité...")
        
        try:
            self.visualizer.clear()
            self.visualizer.draw_connectivity_analysis(self.current_graph, self.current_results)
            self.visualizer.show()
            
        except Exception as e:
            print(f"❌ Erreur lors de la visualisation: {e}")
    
    def visualize_k_comparison(self) -> None:
        """
        Visualise la comparaison k-connexité
        """
        if not self.current_graph:
            print("❌ Aucun graphe chargé.")
            return
        
        if not self.current_results:
            print("⚠️ Aucune analyse disponible. Lancement de l'analyse...")
            if not self.analyze_connectivity():
                return
        
        print("\n🎨 Génération de la comparaison k-connexité...")
        
        max_k_display = input("📊 Nombre de valeurs k à comparer (défaut: 5): ").strip()
        try:
            max_k_display = int(max_k_display) if max_k_display else 5
        except ValueError:
            max_k_display = 5
        
        try:
            self.visualizer.clear()
            self.visualizer.draw_k_connectivity_comparison(self.current_graph, self.current_results, max_k_display)
            self.visualizer.show()
            
        except Exception as e:
            print(f"❌ Erreur lors de la visualisation: {e}")
    
    def export_results(self) -> None:
        """
        Exporte les résultats de l'analyse
        """
        if not self.current_results:
            print("❌ Aucune analyse disponible. Veuillez d'abord effectuer une analyse.")
            return
        
        print("\n💾 EXPORT DES RÉSULTATS")
        print("="*30)
        
        # Choix du format
        print("\n📋 Formats disponibles:")
        print("   1. JSON (données structurées)")
        print("   2. TXT (résumé lisible)")
        
        format_choice = input("\n🎯 Format d'export (1 ou 2): ").strip()
        format_type = 'json' if format_choice == '1' else 'txt'
        extension = 'json' if format_choice == '1' else 'txt'
        
        # Chemin de sauvegarde
        default_filename = f"connectivity_analysis.{extension}"
        filepath = input(f"\n📁 Nom du fichier (défaut: {default_filename}): ").strip()
        
        if not filepath:
            filepath = default_filename
        
        # Export
        try:
            success = self.analyzer.export_results(filepath, format_type)
            if success:
                print(f"✅ Résultats exportés vers: {filepath}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'export: {e}")
    
    def _display_graph_info(self) -> None:
        """
        Affiche les informations sur le graphe actuel
        """
        if not self.current_graph:
            print("❌ Aucun graphe chargé.")
            return
        
        print("\n📊 INFORMATIONS SUR LE GRAPHE ACTUEL")
        print("="*40)
        print(f"   • Nombre de nœuds: {self.current_graph.number_of_nodes()}")
        print(f"   • Nombre d'arêtes: {self.current_graph.number_of_edges()}")
        print(f"   • Type: {'Orienté' if self.current_graph.is_directed() else 'Non orienté'}")
        print(f"   • Connexe: {'Oui' if nx.is_connected(self.current_graph) else 'Non'}")
        
        # Nœuds (limité à 20 pour éviter l'encombrement)
        nodes = list(self.current_graph.nodes())
        if len(nodes) <= 20:
            print(f"   • Nœuds: {nodes}")
        else:
            print(f"   • Nœuds: {nodes[:10]}... (et {len(nodes)-10} autres)")
    
    def display_help(self) -> None:
        """
        Affiche l'aide détaillée
        """
        help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                AIDE DÉTAILLÉE                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔍 CONCEPTS DE K-CONNEXITÉ:

📌 Connexité par nœuds κ(G):
   • Nombre minimum de nœuds à supprimer pour déconnecter le graphe
   • Un graphe est k-connexe par nœuds si κ(G) ≥ k

📌 Connexité par arêtes λ(G):
   • Nombre minimum d'arêtes à supprimer pour déconnecter le graphe
   • Un graphe est k-connexe par arêtes si λ(G) ≥ k

📌 Relation fondamentale:
   • κ(G) ≤ λ(G) ≤ δ(G) où δ(G) est le degré minimum

🛠️ UTILISATION DU PROGRAMME:

1️⃣ CHARGEMENT DE GRAPHES:
   • Fichiers EdgeList: une arête par ligne (format: nœud1 nœud2)
   • Fichiers GML/GraphML: formats standard NetworkX
   • Création manuelle: saisie interactive des arêtes
   • Graphes d'exemple: collection de graphes classiques

2️⃣ ANALYSE:
   • Calcul automatique de κ(G) et λ(G)
   • Identification des coupes minimales
   • Test de k-connexité pour différentes valeurs de k

3️⃣ VISUALISATION:
   • Graphe de base avec différents layouts
   • Visualisation des coupes minimales (nœuds/arêtes en rouge)
   • Comparaison visuelle pour différentes valeurs de k

4️⃣ EXPORT:
   • JSON: données complètes pour traitement ultérieur
   • TXT: résumé lisible pour rapport

💡 CONSEILS:
   • Utilisez les graphes d'exemple pour vous familiariser
   • Pour de gros graphes, limitez la valeur maximale de k
   • La visualisation est optimale pour des graphes < 50 nœuds
   • Les calculs peuvent être longs pour des graphes très denses

❓ INTERPRÉTATION DES RÉSULTATS:
   • κ(G) = 0: graphe non connexe ou trivial
   • κ(G) = 1: graphe connexe avec points d'articulation
   • κ(G) ≥ 2: graphe robuste, pas de point de défaillance unique
   • Plus κ(G) et λ(G) sont élevés, plus le graphe est robuste

═══════════════════════════════════════════════════════════════════════════════
        """
        print(help_text)
    
    def run(self) -> None:
        """
        Lance l'interface utilisateur principale
        """
        self.display_welcome()
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\n🎯 Votre choix: ").strip()
                
                if choice == '0':
                    print("\n👋 Au revoir! Merci d'avoir utilisé l'analyseur de k-connexité.")
                    break
                    
                elif choice == '1':
                    self.load_graph_from_file()
                    
                elif choice == '2':
                    self.create_graph_manually()
                    
                elif choice == '3':
                    self.use_example_graph()
                    
                elif choice == '4':
                    self.analyze_connectivity()
                    
                elif choice == '5':
                    self.visualize_graph()
                    
                elif choice == '6':
                    self.visualize_connectivity()
                    
                elif choice == '7':
                    self.visualize_k_comparison()
                    
                elif choice == '8':
                    self.export_results()
                    
                elif choice == '9':
                    self._display_graph_info()
                    
                elif choice == '10':
                    self.display_help()
                    
                else:
                    print("❌ Choix invalide. Veuillez choisir une option valide.")
                
                # Pause avant de continuer
                if choice != '0':
                    input("\n⏸️ Appuyez sur Entrée pour continuer...")
                    print("\n" * 2)  # Espacement
                    
            except KeyboardInterrupt:
                print("\n\n👋 Interruption détectée. Au revoir!")
                break
            except Exception as e:
                print(f"\n❌ Erreur inattendue: {e}")
                input("\n⏸️ Appuyez sur Entrée pour continuer...")

def main():
    """
    Fonction principale
    """
    try:
        # Vérification des dépendances
        required_modules = ['networkx', 'matplotlib', 'numpy']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"❌ Modules manquants: {', '.join(missing_modules)}")
            print("💡 Installez-les avec: pip install networkx matplotlib numpy")
            return
        
        # Lancement de l'interface
        interface = GraphConnectivityInterface()
        interface.run()
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
