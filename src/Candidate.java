import java.util.List;

public record Candidate(List<String> row, String gender, String group,
                        double math, double english, double computer, double average) {
    public Candidate {
        row = List.copyOf(row);
    }
}
