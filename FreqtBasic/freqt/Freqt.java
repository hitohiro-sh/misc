package freqt;

import java.io.*;
import java.util.*;


public class Freqt {
	private BufferedReader in;
	private int support; // minsup
	private boolean outputPattern;

	private static class DepthLabelPair {
		private int depth;
		private int label;
		// private String label;
		
		public static DepthLabelPair newWithDepthLabel(int depth, int label) {

			return new DepthLabelPair(depth, label);
		}
		
		public DepthLabelPair(int depth, String label) {
			this.depth = depth;
			this.label = Integer.parseInt(label);
		}
		
		public DepthLabelPair(int depth, int label) {
			this.label = label;
			this.depth = depth;
		}
		
		public boolean equals(Object obj) {
			DepthLabelPair p = (DepthLabelPair)obj;
			
			if (this.depth != p.depth) {
				return false;
			}
			return (this.label == p.label);
			// return this.label.equals(p.label);
		}
		
		public int hashCode() {
			return label + depth * 1000;
		}

		public String toString() {
			StringBuilder sb = new StringBuilder();
			sb.append(this.depth);
			sb.append(':');
			sb.append(this.label); 
			return sb.toString();
		}
	}
	
	private class Node {
		private int tid;
		private int labelID;
		private Node parent;
		int index; //childs[index] of parent

		private ArrayList<Node> childs;
		
		private Node(int tid) {}

		public Node(String strlabelID, int tid) {
			this.labelID = Integer.parseInt(strlabelID);
			this.childs = null;
			this.parent = null;
			this.index = -1;
			this.tid = tid;
		}
		
		public void addChild(Node node) {
			if (childs != null) {
				childs.add(node);
			} else {
				childs = new ArrayList<Node>();
				childs.add(node);
			}
			node.index = childs.size() - 1;
			node.parent = this;
		}
		
		public Node nextSibling() {
			if (this.parent == null) {
				return null;
			}
			
			if (this.parent.childs.size() - 1 > this.index) {
				return this.parent.childs.get(this.index + 1);
			}
			return null;
		}
	}
	
	private static class Projected {
	
		private int lastTid;
		private int depth;
		private int support;
		private List<Node> locations;
		private List<DepthLabelPair> pattern;
		
		public Projected(int depth) {
			this.depth = depth;
			support = 0;
			locations = new ArrayList<Node>();
			lastTid = -1;
			pattern = new ArrayList<>();
		}
		
		public Projected(Node node, DepthLabelPair pair) {
			depth = 0;
			support = 1;
			locations = new ArrayList<Node>();
			pattern = new ArrayList<>();

			lastTid = node.tid;
			locations.add(node);
			pattern.add(pair);
		}

		public Projected(Node node, Projected p, DepthLabelPair pair) {
			depth = 0;
			support = 1;
			locations = new ArrayList<Node>();
			pattern = new ArrayList<>();

			lastTid = node.tid;
			locations.add(node);
			pattern.addAll(p.getPattern());
			pattern.add(pair);
		}
		
		public void addNode(Node node) {
			if (this.lastTid != node.tid) {
				support++;
				this.lastTid = node.tid;
			}
			this.locations.add(node);
		}
		
		public int size() {
			return this.locations.size();
		}
		
		public int support() {
			return this.support;
		}

		public List<DepthLabelPair> getPattern() {
			return this.pattern;
		}
		
	}

	public class Tree implements Iterable<Node> {
		int tid;
		private List<Node> nodeArray;
		
		private Tree() {}
		
		public Tree(Node root, int tid) {
			nodeArray = new ArrayList<Node>();
			nodeArray.add(root);
			this.tid = tid;
		}

		public List<Node> nodes() {
			return nodeArray;
		}
		
		public int size() {
			return nodeArray.size();
		}
		
		public Iterator<Node> iterator() {
			return nodeArray.iterator();
		}
	}
	
	private class Database implements Iterable<Tree> {
		private List<Tree> treeArray;
		
		private Database() {
			treeArray = new ArrayList<Tree>();
		}
		
		private Database(int maxSize) {
			treeArray = new ArrayList<Tree>(maxSize);
		}
		
		public Tree get(int index) {
			return treeArray.get(index);
		}
		
		public void add(Tree tree) {
			treeArray.add(tree);
		}
		
		public int size() {
			return treeArray.size(); 
		}
		
		public Iterator<Tree> iterator() {
			return treeArray.iterator();
		}
	}
	
	private Database database;
	private int totalPatternNum;
	
	private Freqt() {
		super();
	}
	
	private void init(int support, BufferedReader in) {
		this.support = support;
		this.in = in;
		totalPatternNum = 0;		
	}
	
	public Freqt(int support, BufferedReader in, boolean outputPattern) {
		this.outputPattern = outputPattern;
		init(support, in);
	}
	
	private Database readTree() throws Exception {
		String buf;
		Database database = new Database();

		int line = 0;
		int maxSize = 0;
		int tid = 0;
		
		try {
		
			while ((buf = in.readLine()) != null) {
				String[] strArray = buf.split("\\s+");
				String labelID = strArray[3];
				
				Node currentNode = new Node(labelID, tid);
				Tree tree = new Tree(currentNode, tid);

				for (int i = 4; i < strArray.length; i++) {
					String tmp = strArray[i];
					if (tmp.equals("-1")) {
						currentNode = currentNode.parent;
						continue;
					}
					Node node = new Node(tmp, tid);
					tree.nodes().add(node);
					currentNode.addChild(node);
					currentNode = node;
				}
				line++;
				database.add(tree);
				if (tree.size() > maxSize) {
					maxSize = tree.size();
				}
				tid++;
			}
		} catch (Error error) {
			System.err.println("readTree: line:" + line);
			error.printStackTrace();
			System.exit(1);
		}
		System.err.println("end readTree: line: " + line + " maxSize: " + maxSize);
		
		return database;
	}
	
	private void prune(Map<DepthLabelPair, Projected> rmo) {
		Collection<DepthLabelPair> labelSet = new ArrayList<DepthLabelPair>(rmo.keySet());
		
		for (DepthLabelPair labelIDDepthPair : labelSet) {
			Projected p = rmo.get(labelIDDepthPair);
			if (p.support() < support) {
			    rmo.remove(labelIDDepthPair);
			}
		}
	}
	
	private void setFreq1(HashMap<DepthLabelPair, Projected> rmo) {
		for (Tree tree : database) {
			for (Node node : tree) {
				DepthLabelPair pair = DepthLabelPair.newWithDepthLabel(0, node.labelID);

				Projected p = rmo.get(pair);
				if (p != null) {
				  	p.addNode(node);
				} else {
				  	rmo.put(pair, new Projected(node, pair));
				}
			}
		}
		prune(rmo);
	}
	
	private void run() throws Exception {
		long readStart = System.nanoTime();
		database = readTree();
		long readEnd = System.nanoTime();
		System.err.println("read time: " + (readEnd - readStart));
		
		HashMap<DepthLabelPair, Projected> rmo = new HashMap<DepthLabelPair, Projected>();
		setFreq1(rmo);
		expand(rmo);

		System.out.println("totalPatternNum = " + totalPatternNum);
		long end = System.nanoTime();
		System.err.println("run time: " + (end - readEnd) / 1000000000.0);
	}
	

	private void project(Projected projected) {
		int depth = projected.depth;
		// Node[] branch = new Node[depth + 1];
		HashMap<DepthLabelPair, Projected> candidate = new HashMap<DepthLabelPair, Projected>();
		
		for (Node node : projected.locations) {
			Node pos = node;
			int start = 0;
			for (int d = -1; d < depth && pos != null; d++) {
				ArrayList<Node> childs;
				
				// if(branch[d + 1] != pos) { // duplicate test
					// branch[d + 1] = pos;

					childs = pos.childs;
					int newdepth = depth - d;
					
					for (int l = start; childs != null && l < childs.size(); l++) {
						Node target = childs.get(l);
						
						DepthLabelPair pair = DepthLabelPair.newWithDepthLabel(newdepth, target.labelID);
						Projected p = candidate.get(pair);
						if (p != null) {
							p.addNode(target);
						} else {
							candidate.put(pair, new Projected(target, projected, pair));
						}
						candidate.get(pair).depth = newdepth;
					}
				// }
				start = pos.index + 1;
				pos = pos.parent;
			}
		}
		
		prune(candidate);
		expand(candidate);
	}
	
	
	private void expand(Map<DepthLabelPair, Projected> rmo) {
		Map<DepthLabelPair, Projected> occ = rmo;
		Set<Map.Entry<DepthLabelPair, Projected>> set = occ.entrySet();
		
		for (Map.Entry<DepthLabelPair, Projected> entry : set) {

			totalPatternNum++;
			Projected projected = entry.getValue();
			if (this.outputPattern) {
				for (DepthLabelPair pair : projected.getPattern()) {
					System.out.print(pair + " ");
				}
				System.out.println();
			}
			project(projected);
		}
	}
	
	public static void main(String[] args) throws Exception {
		if (args.length < 2) {
			System.out.println("Usage: java Freqt support infile");
			System.exit(0);
		}
		boolean outputPattern = false;
		if (args.length > 2) {
			if (args[2].equals("--outputpattern")) {
				outputPattern = true;
			}
		}

		int support = Integer.parseInt(args[0]); // new Integer(args[0]);
		System.err.println("support: " + support);
		String inFileName = args[1];
		System.err.println(inFileName);
		BufferedReader in = new BufferedReader(new FileReader(inFileName));
		Freqt freqt = new Freqt(support, in, outputPattern);
		freqt.run();
		
		in.close();
	}

}
