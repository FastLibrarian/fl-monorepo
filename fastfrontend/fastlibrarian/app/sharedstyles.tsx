import { StyleSheet } from "react-native";

export const sharedStyles = StyleSheet.create({
  container: { flex: 1, padding: 24 },

  title: {
    fontSize: 28,
    marginBottom: 16,
    alignSelf: "center",
    fontWeight: "bold",
  },

  subtitle: { fontSize: 20, marginTop: 24 },

  textInput: {
    borderWidth: 1,
    borderColor: "#ccc",
    marginVertical: 8,
    padding: 8,
    borderRadius: 4,
  },

  listItem: { fontSize: 16, marginVertical: 4 },

  addButton: {
    color: "#fff",
    backgroundColor: "#007AFF",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 4,
    overflow: "hidden",
    marginLeft: 8,
  },
  card: {
    backgroundColor: "#fff",
    borderRadius: 8,
    padding: 16,
    marginVertical: 8,
    marginHorizontal: "10%",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    flexDirection: "column",
    alignItems: "flex-start",
    justifyContent: "space-between",
  },
  primaryName: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 4,
  },
  primaryText: {
    fontSize: 14,
    color: "#555",
    marginBottom: 8,
  },
  secondaryName: {
    fontSize: 16,
    fontStyle: "italic",
    fontWeight: "normal",
    marginBottom: 4,
  },
  tertiaryText: {
    fontSize: 14,
    color: "#777",
    marginBottom: 4,
    fontStyle: "italic",
  },
  inDbLabel: {
    color: "green",
    fontWeight: "bold",
  },
  searchInput: {
    margin: 16,
    padding: 8,
    borderWidth: 1,
    borderRadius: 8,
    borderColor: "#ccc",
  },
  searchOverlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "#fff",
    zIndex: 10,
    padding: 16,
  },
  expandedSearchInput: {
    padding: 12,
    borderWidth: 1,
    borderRadius: 8,
    borderColor: "#007AFF",
    marginBottom: 16,
    fontSize: 18,
  },
});
