import React, { useState } from "react";
import {
  View,
  Text,
  Pressable,
  StyleProp,
  ViewStyle,
  Modal,
  TouchableOpacity,
} from "react-native";
import { sharedStyles as styles } from "../app/sharedstyles";
import { useRouter } from "expo-router";

// Book status enum matching the API
enum BookStatus {
  Wanted = "Wanted",
  Have = "Have",
  Ignored = "Ignored",
  Delete = "Delete",
}

interface BookCardProps {
  book: {
    id: string;
    title: string;
    description?: string | null;
    authors?: { id: string; name: string }[];
    series?:
      | { id: string; name: string }[]
      | { id: string; name: string }
      | null;
    status?: BookStatus | null; // E-book status
    a_status?: BookStatus | null; // Audio book status
    p_status?: BookStatus | null; // Physical book status
  };
  onPressDetails?: () => void;
  showDetailsButton?: boolean;
  containerStyle?: StyleProp<ViewStyle>;
  onStatusChange?: (
    type: "ebook" | "audio" | "physical",
    status: BookStatus
  ) => void;
  activeDropdown?: { bookId: string; type: string } | null;
  onDropdownToggle?: (bookId: string, type: string) => void;
}

// Status Dropdown Component
const StatusDropdown: React.FC<{
  label: string;
  value: BookStatus | null;
  onValueChange: (status: BookStatus) => void;
  isOpen: boolean;
  onToggle: () => void;
}> = ({ label, value, onValueChange, isOpen, onToggle }) => {
  const statusOptions = Object.values(BookStatus);

  return (
    <View style={{ marginVertical: 4 }}>
      <Text style={[styles.tertiaryText, { fontSize: 12 }]}>{label}:</Text>
      <Pressable
        onPress={onToggle}
        style={{
          borderWidth: 1,
          borderColor: "#ccc",
          borderRadius: 4,
          paddingHorizontal: 25,
          paddingVertical: 4,
          backgroundColor: "#f9f9f9",
          minHeight: 32,
          justifyContent: "center",
          flexDirection: "row",
          alignItems: "center",
        }}
      >
        <Text style={[styles.primaryText, { fontSize: 14, flex: 1 }]}>
          {value || "Select status"}
        </Text>
        <Text style={[styles.primaryText, { fontSize: 12 }]}>
          {isOpen ? " ▲" : " ▼"}
        </Text>
      </Pressable>

      {isOpen && (
        <View
          style={{
            marginTop: 2,
            backgroundColor: "white",
            borderWidth: 1,
            borderColor: "#ccc",
            borderRadius: 4,
            elevation: 8,
            shadowColor: "#000",
            shadowOffset: { width: 0, height: 4 },
            shadowOpacity: 0.3,
            shadowRadius: 6,
          }}
        >
          {statusOptions.map((status) => (
            <Pressable
              key={status}
              onPress={() => {
                onValueChange(status);
              }}
              style={{
                paddingVertical: 8,
                paddingHorizontal: 12,
                borderBottomWidth:
                  status === statusOptions[statusOptions.length - 1] ? 0 : 1,
                borderBottomColor: "#eee",
              }}
            >
              <Text
                style={[
                  styles.primaryText,
                  { fontSize: 14 },
                  value === status && {
                    fontWeight: "bold",
                    color: "#007AFF",
                  },
                ]}
              >
                {status}
              </Text>
            </Pressable>
          ))}
        </View>
      )}
    </View>
  );
};

const BookCard: React.FC<BookCardProps> = ({
  book,
  onPressDetails,
  showDetailsButton = true,
  containerStyle,
  onStatusChange,
  activeDropdown,
  onDropdownToggle,
}) => {
  const router = useRouter();
  const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false);

  // Debug: Log status values
  console.log("Book statuses for", book.title, ":", {
    status: book.status,
    a_status: book.a_status,
    p_status: book.p_status,
  });

  // Support both array and single object for series
  const seriesList = Array.isArray(book.series)
    ? book.series
    : book.series
    ? [book.series]
    : [];

  const handlePress = onPressDetails
    ? onPressDetails
    : () => router.navigate({ pathname: "/book", params: { id: book.id } });

  const handleStatusChange = (
    type: "ebook" | "audio" | "physical",
    status: BookStatus
  ) => {
    if (onStatusChange) {
      onStatusChange(type, status);
    }
  };

  const handleDropdownToggle = (type: string) => {
    if (onDropdownToggle) {
      onDropdownToggle(book.id, type);
    }
  };

  return (
    <View style={[styles.card, containerStyle]}>
      <Pressable onPress={handlePress}>
        <Text style={[styles.primaryName, { textDecorationLine: "underline" }]}>
          {book.title}
        </Text>
      </Pressable>
      {book.authors && book.authors.length > 0 && (
        <Text style={styles.secondaryName}>
          {book.authors.map((a) => a.name).join(", ")}
        </Text>
      )}

      {/* Expandable Description */}
      {book.description ? (
        <View>
          <Text
            style={styles.primaryText}
            numberOfLines={isDescriptionExpanded ? undefined : 4}
          >
            {book.description}
          </Text>
          {book.description.length > 200 && ( // Rough estimate for 4 lines
            <Pressable
              onPress={() => setIsDescriptionExpanded(!isDescriptionExpanded)}
              style={{ marginTop: 4 }}
            >
              <Text
                style={[
                  styles.tertiaryText,
                  { fontStyle: "italic", fontSize: 12 },
                ]}
              >
                {isDescriptionExpanded ? "Show less" : "Show more"}
              </Text>
            </Pressable>
          )}
        </View>
      ) : (
        <Text style={styles.tertiaryText}>(No description)</Text>
      )}

      {seriesList.length > 0 && (
        <Text style={styles.secondaryName}>
          Series: {seriesList.map((s) => s.name).join(", ")}
        </Text>
      )}

      {/* Status Dropdowns */}
      <View
        style={{
          marginTop: 12,
          marginLeft: 8,
          overflow: "visible",
          flexDirection: "row",
          flex: 3,
          justifyContent: "center",
        }}
      >
        <StatusDropdown
          label="E-book Status"
          value={book.status || null}
          onValueChange={(status) => handleStatusChange("ebook", status)}
          isOpen={
            activeDropdown?.bookId === book.id &&
            activeDropdown?.type === "ebook"
          }
          onToggle={() => handleDropdownToggle("ebook")}
        />
        <StatusDropdown
          label="Audiobook Status"
          value={book.a_status || null}
          onValueChange={(status) => handleStatusChange("audio", status)}
          isOpen={
            activeDropdown?.bookId === book.id &&
            activeDropdown?.type === "audio"
          }
          onToggle={() => handleDropdownToggle("audio")}
        />
        <StatusDropdown
          label="Physical Book Status"
          value={book.p_status || null}
          onValueChange={(status) => handleStatusChange("physical", status)}
          isOpen={
            activeDropdown?.bookId === book.id &&
            activeDropdown?.type === "physical"
          }
          onToggle={() => handleDropdownToggle("physical")}
        />
      </View>
    </View>
  );
};

export default BookCard;
