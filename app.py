from state_graph import build_graph
import time

def main():
    print("🚀 Starting Vision-Based Wordle Agent...\n")

    graph = build_graph()
    time.sleep(5)

    final_state = graph.invoke({})

    print("\n✅ Game Finished!")
    print("🧾 Final State Summary:")
    
    for k, v in final_state.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()