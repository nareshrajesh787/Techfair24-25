# Import necessary models
from django.contrib.auth.models import User
from home.models import Assignment, Review
from django.utils import timezone


#pwds teacher123 student123

def run():
    # Create test users

    # Get user objects
    mrs_anderson = User.objects.get(username='mrs_anderson')
    dr_parker = User.objects.get(username='dr_parker')
    mr_singh = User.objects.get(username='mr_singh')
    emma = User.objects.get(username='emma_student')
    james = User.objects.get(username='james_student')
    sophia = User.objects.get(username='sophia_student')

    assignments = [
        {
            "title": "The Great Gatsby Literary Analysis",
            "description": "Write a 1500-word analysis exploring the symbolism of color and the American Dream in F. Scott Fitzgerald's The Great Gatsby.",
            "course": "AP Literature",
            "assignment_type": "Essay",
            "author": mrs_anderson,
            "uploaded_assignment": "assignments/GatsbyAnalysis.docx",
            "num_criteria": 4,
            "rubric": {
                "Literary Analysis": {"description": "Depth of analysis and interpretation", "max_points": 25},
                "Evidence": {"description": "Use of textual evidence", "max_points": 25},
                "Writing": {"description": "Clear academic writing style", "max_points": 25},
                "Organization": {"description": "Logical structure and flow", "max_points": 25}
            },
            "is_published": True
        },
        {
            "title": "Cell Membrane Lab Report",
            "description": "Document your findings from our membrane permeability experiment. Include methodology, data analysis, and conclusions.",
            "course": "AP Biology",
            "assignment_type": "Lab Report",
            "author": dr_parker,
            "uploaded_assignment": "assignments/CellLab.docx",
            "num_criteria": 4,
            "rubric": {
                "Scientific Method": {"description": "Proper experimental procedure", "max_points": 25},
                "Data Analysis": {"description": "Accurate data interpretation", "max_points": 25},
                "Conclusions": {"description": "Well-reasoned conclusions", "max_points": 25},
                "Format": {"description": "Professional lab report format", "max_points": 25}
            },
            "is_published": True
        },
        {
            "title": "Civil Rights Movement Research",
            "description": "Research and analyze a key figure from the Civil Rights Movement. Evaluate their contributions, challenges faced, and lasting impact.",
            "course": "US History",
            "assignment_type": "Essay",
            "author": mr_singh,
            "uploaded_assignment": "assignments/CivilRights.docx",
            "num_criteria": 4,
            "rubric": {
                "Historical Accuracy": {"description": "Factual correctness", "max_points": 25},
                "Analysis": {"description": "Critical thinking", "max_points": 25},
                "Sources": {"description": "Quality of sources", "max_points": 25},
                "Presentation": {"description": "Clear communication", "max_points": 25}
            },
            "is_published": True
        },
        {
            "title": "Python Game Development",
            "description": "Create a text-based game using Python. Must include classes, functions, and proper documentation.",
            "course": "Computer Science",
            "assignment_type": "Project",
            "author": dr_parker,
            "uploaded_assignment": "assignments/PythonGame.docx",
            "num_criteria": 4,
            "rubric": {
                "Functionality": {"description": "Working game mechanics", "max_points": 25},
                "Code Quality": {"description": "Clean, efficient code", "max_points": 25},
                "Documentation": {"description": "Clear comments and instructions", "max_points": 25},
                "Creativity": {"description": "Original game concept", "max_points": 25}
            },
            "is_published": True
        },
        {
            "title": "Environmental Impact Study",
            "description": "Analyze human impact on local ecosystems. Include field research, data collection, and proposed solutions.",
            "course": "Environmental Science",
            "assignment_type": "Lab Report",
            "author": dr_parker,
            "uploaded_assignment": "assignments/Environment.docx",
            "num_criteria": 4,
            "rubric": {
                "Research Methods": {"description": "Data collection techniques", "max_points": 25},
                "Analysis": {"description": "Data interpretation", "max_points": 25},
                "Solutions": {"description": "Practical recommendations", "max_points": 25},
                "Presentation": {"description": "Professional report format", "max_points": 25}
            },
            "is_published": True
        }
    ]

    reviews = [
        {
            "assignment": "The Great Gatsby Literary Analysis",
            "reviewer": emma,
            "feedback": "Excellent analysis of symbolism. Strong connection between the green light and Gatsby's dreams. Consider including more direct quotes to support your interpretations.",
            "rubric_scores": {
                "Literary Analysis": 22,
                "Evidence": 20,
                "Writing": 23,
                "Organization": 24
            },
            "final_percent": 89.0
        },
        {
            "assignment": "Cell Membrane Lab Report",
            "reviewer": james,
            "feedback": "Well-structured methodology and clear data presentation. The discussion section could delve deeper into the implications of your findings.",
            "rubric_scores": {
                "Scientific Method": 24,
                "Data Analysis": 22,
                "Conclusions": 20,
                "Format": 25
            },
            "final_percent": 91.0
        },
        {
            "assignment": "Civil Rights Movement Research",
            "reviewer": sophia,
            "feedback": "Thorough research and strong analysis. The connection to modern social movements was particularly insightful. Consider expanding on the long-term impact.",
            "rubric_scores": {
                "Historical Accuracy": 25,
                "Analysis": 23,
                "Sources": 24,
                "Presentation": 22
            },
            "final_percent": 94.0
        },
        {
            "assignment": "Python Game Development",
            "reviewer": emma,
            "feedback": "Creative game concept and clean code implementation. Could benefit from more detailed user instructions and error handling.",
            "rubric_scores": {
                "Functionality": 23,
                "Code Quality": 24,
                "Documentation": 21,
                "Creativity": 25
            },
            "final_percent": 93.0
        },
        {
            "assignment": "Environmental Impact Study",
            "reviewer": james,
            "feedback": "Comprehensive data collection and analysis. The proposed solutions are practical and well-thought-out. Consider adding more visual representations of data.",
            "rubric_scores": {
                "Research Methods": 24,
                "Analysis": 23,
                "Solutions": 25,
                "Presentation": 22
            },
            "final_percent": 94.0
        }
    ]

    reviews.extend([
    # Additional Gatsby Reviews
    {
        "assignment": "The Great Gatsby Literary Analysis",
        "reviewer": james,
        "feedback": "Good grasp of symbolism but needs more historical context. The analysis of the green light is compelling, though the connection to the American Dream could be stronger. Include more evidence from secondary sources.",
        "rubric_scores": {
            "Literary Analysis": 21,
            "Evidence": 19,
            "Writing": 24,
            "Organization": 22
        },
        "final_percent": 86.0
    },
    {
        "assignment": "The Great Gatsby Literary Analysis",
        "reviewer": sophia,
        "feedback": "Strong writing style and excellent organization. The analysis of color symbolism is particularly insightful. Consider exploring the social class dynamics more deeply.",
        "rubric_scores": {
            "Literary Analysis": 24,
            "Evidence": 23,
            "Writing": 25,
            "Organization": 24
        },
        "final_percent": 96.0
    },

    # Additional Cell Lab Reviews
    {
        "assignment": "Cell Membrane Lab Report",
        "reviewer": sophia,
        "feedback": "Excellent methodology section. Data visualization could be improved with clearer graphs. Statistical analysis is thorough and well-explained.",
        "rubric_scores": {
            "Scientific Method": 25,
            "Data Analysis": 21,
            "Conclusions": 23,
            "Format": 24
        },
        "final_percent": 93.0
    },
    {
        "assignment": "Cell Membrane Lab Report",
        "reviewer": emma,
        "feedback": "Strong experimental design but some procedural steps could be clearer. Results are well-analyzed and the discussion shows good understanding of concepts.",
        "rubric_scores": {
            "Scientific Method": 23,
            "Data Analysis": 24,
            "Conclusions": 22,
            "Format": 23
        },
        "final_percent": 92.0
    },

    # Additional Civil Rights Reviews
    {
        "assignment": "Civil Rights Movement Research",
        "reviewer": james,
        "feedback": "Excellent use of primary sources. The analysis of leadership styles is particularly strong. Consider adding more about the movement's influence on later social movements.",
        "rubric_scores": {
            "Historical Accuracy": 24,
            "Analysis": 25,
            "Sources": 25,
            "Presentation": 23
        },
        "final_percent": 97.0
    },
    {
        "assignment": "Civil Rights Movement Research",
        "reviewer": emma,
        "feedback": "Well-researched and thoughtfully presented. The timeline could be more clearly organized, but the analysis of key events is strong.",
        "rubric_scores": {
            "Historical Accuracy": 23,
            "Analysis": 22,
            "Sources": 24,
            "Presentation": 21
        },
        "final_percent": 90.0
    },

    # Additional Python Game Reviews
    {
        "assignment": "Python Game Development",
        "reviewer": sophia,
        "feedback": "Innovative game mechanics and clean code structure. Could use more extensive error handling and input validation. Documentation is clear and helpful.",
        "rubric_scores": {
            "Functionality": 24,
            "Code Quality": 23,
            "Documentation": 22,
            "Creativity": 25
        },
        "final_percent": 94.0
    },
    {
        "assignment": "Python Game Development",
        "reviewer": james,
        "feedback": "Excellent game design and user interface. Code is well-organized but could be more modular. Great balance of creativity and functionality.",
        "rubric_scores": {
            "Functionality": 25,
            "Code Quality": 22,
            "Documentation": 23,
            "Creativity": 24
        },
        "final_percent": 94.0
    },

    # Additional Environmental Study Reviews
    {
        "assignment": "Environmental Impact Study",
        "reviewer": sophia,
        "feedback": "Comprehensive data collection methodology. The analysis is thorough and the proposed solutions are realistic. Excellent use of visual aids.",
        "rubric_scores": {
            "Research Methods": 25,
            "Analysis": 24,
            "Solutions": 24,
            "Presentation": 25
        },
        "final_percent": 98.0
    },
    {
        "assignment": "Environmental Impact Study",
        "reviewer": emma,
        "feedback": "Strong research approach and detailed analysis. Some solutions could be more specific to the local context. Data presentation is clear and effective.",
        "rubric_scores": {
            "Research Methods": 23,
            "Analysis": 24,
            "Solutions": 22,
            "Presentation": 24
        },
        "final_percent": 93.0
    }
])

    # Create assignments
    created_assignments = {}
    for assignment_data in assignments:
        rubric = assignment_data.pop('rubric')
        title = assignment_data["title"]
        assignment = Assignment.objects.create(**assignment_data)
        assignment.rubric = rubric
        assignment.save()
        created_assignments[title] = assignment

    # Create reviews
    for review_data in reviews:
        assignment_title = review_data.pop("assignment")
        assignment = created_assignments[assignment_title]
        Review.objects.create(assignment=assignment, **review_data)

if __name__ == '__main__':
    run()
