import java.util.List;

/** IDs remain strings so leading zeroes survive CSV round trips. */
public record Student(String name, String id, String gender) {
    public Student {
        if (name == null || id == null || gender == null
                || name.isBlank() || id.isBlank() || gender.isBlank()) {
            throw new IllegalArgumentException("Student name, ID, and gender must not be blank.");
        }
    }

    public List<String> toRow() {
        return List.of(name, id, gender);
    }

    @Override
    public String toString() {
        return String.format("Name: %s | ID: %s | Gender: %s", name, id, gender);
    }
}
