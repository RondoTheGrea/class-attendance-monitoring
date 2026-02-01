import { useState } from "react";
import { Button } from "@/app/components/ui/button";
import { Plus, GraduationCap, BookOpen } from "lucide-react";
import { CreateClassModal } from "@/app/components/CreateClassModal";
import { ClassCard } from "@/app/components/ClassCard";
import { ClassDetailView } from "@/app/components/ClassDetailView";

interface Schedule {
  day: string;
  startTime: string;
  endTime: string;
}

interface Announcement {
  id: string;
  title: string;
  content: string;
  createdAt: string;
}

interface AttendanceRecord {
  id: string;
  date: string;
  scheduleTime: string;
  students: Array<{
    id: string;
    name: string;
    studentId: string;
    timeScanned: string;
  }>;
}

interface ClassData {
  id: string;
  subject: string;
  section?: string;
  room?: string;
  description?: string;
  schedules: Schedule[];
  announcements: Announcement[];
  attendance: AttendanceRecord[];
}

// Mock data for demonstration
const initialClasses: ClassData[] = [
  {
    id: "1",
    subject: "Introduction to Computer Science",
    section: "A",
    room: "Room 301",
    description: "Fundamentals of computer science including programming, algorithms, and data structures.",
    schedules: [
      { day: "Monday", startTime: "09:00", endTime: "10:30" },
      { day: "Wednesday", startTime: "09:00", endTime: "10:30" },
      { day: "Friday", startTime: "09:00", endTime: "10:30" }
    ],
    announcements: [
      {
        id: "a1",
        title: "Midterm Exam Schedule",
        content: "The midterm examination will be held on February 15, 2026. Please review chapters 1-5.",
        createdAt: "2026-01-28T10:00:00Z"
      },
      {
        id: "a2",
        title: "Project Submission Reminder",
        content: "Don't forget to submit your programming project by Friday. Late submissions will incur a 10% penalty per day.",
        createdAt: "2026-01-25T14:30:00Z"
      }
    ],
    attendance: [
      {
        id: "att1",
        date: "2026-01-29T09:00:00Z",
        scheduleTime: "09:00 - 10:30",
        students: [
          { id: "s1", name: "Alice Johnson", studentId: "2024-001", timeScanned: "2026-01-29T09:05:00Z" },
          { id: "s2", name: "Bob Smith", studentId: "2024-002", timeScanned: "2026-01-29T09:03:00Z" },
          { id: "s3", name: "Carol Williams", studentId: "2024-003", timeScanned: "2026-01-29T09:07:00Z" }
        ]
      },
      {
        id: "att2",
        date: "2026-01-27T09:00:00Z",
        scheduleTime: "09:00 - 10:30",
        students: [
          { id: "s1", name: "Alice Johnson", studentId: "2024-001", timeScanned: "2026-01-27T09:02:00Z" },
          { id: "s2", name: "Bob Smith", studentId: "2024-002", timeScanned: "2026-01-27T09:04:00Z" }
        ]
      }
    ]
  },
  {
    id: "2",
    subject: "Data Structures and Algorithms",
    section: "B",
    room: "Room 205",
    description: "Advanced study of data structures, algorithm design, and complexity analysis.",
    schedules: [
      { day: "Tuesday", startTime: "14:00", endTime: "15:30" },
      { day: "Thursday", startTime: "14:00", endTime: "15:30" }
    ],
    announcements: [
      {
        id: "a3",
        title: "Lab Session This Week",
        content: "We'll be implementing binary search trees in the lab. Make sure to bring your laptops.",
        createdAt: "2026-01-30T08:00:00Z"
      }
    ],
    attendance: [
      {
        id: "att3",
        date: "2026-01-28T14:00:00Z",
        scheduleTime: "14:00 - 15:30",
        students: [
          { id: "s4", name: "David Brown", studentId: "2024-004", timeScanned: "2026-01-28T14:05:00Z" },
          { id: "s5", name: "Emma Davis", studentId: "2024-005", timeScanned: "2026-01-28T14:02:00Z" }
        ]
      }
    ]
  },
  {
    id: "3",
    subject: "Web Development",
    section: "C",
    room: "Lab 102",
    description: "Modern web development with HTML, CSS, JavaScript, and popular frameworks.",
    schedules: [
      { day: "Monday", startTime: "13:00", endTime: "16:00" },
      { day: "Thursday", startTime: "13:00", endTime: "16:00" }
    ],
    announcements: [],
    attendance: []
  }
];

export default function App() {
  const [classes, setClasses] = useState<ClassData[]>(initialClasses);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [selectedClass, setSelectedClass] = useState<ClassData | null>(null);

  const handleCreateClass = (newClass: ClassData) => {
    setClasses([...classes, newClass]);
  };

  const handleUpdateClass = (updatedClass: ClassData) => {
    setClasses(classes.map(c => c.id === updatedClass.id ? updatedClass : c));
    setSelectedClass(updatedClass);
  };

  const handleClassClick = (classData: ClassData) => {
    setSelectedClass(classData);
  };

  const handleBackToDashboard = () => {
    setSelectedClass(null);
  };

  // If a class is selected, show the detail view
  if (selectedClass) {
    return (
      <ClassDetailView
        classData={selectedClass}
        onBack={handleBackToDashboard}
        onUpdateClass={handleUpdateClass}
      />
    );
  }

  // Otherwise, show the dashboard
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Top Navigation Bar */}
      <div className="bg-white border-b shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-gradient-to-br from-blue-600 to-blue-700 text-white p-2.5 rounded-xl shadow-md">
                <GraduationCap className="h-7 w-7" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">Professor Dashboard</h1>
                <p className="text-sm text-slate-500">Attendance Monitoring System</p>
              </div>
            </div>
            <Button 
              onClick={() => setIsCreateModalOpen(true)} 
              size="lg"
              className="bg-blue-600 hover:bg-blue-700 shadow-sm"
            >
              <Plus className="h-5 w-5 mr-2" />
              Create Class
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {classes.length === 0 ? (
          /* Empty State */
          <div className="flex flex-col items-center justify-center py-24">
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl p-12 mb-6 shadow-sm">
              <BookOpen className="h-20 w-20 text-blue-600" />
            </div>
            <h2 className="text-3xl font-bold text-slate-900 mb-3">Welcome to Your Dashboard</h2>
            <p className="text-slate-600 mb-8 text-center max-w-md leading-relaxed">
              Create your first class to start managing schedules, posting announcements, 
              and tracking student attendance with QR codes.
            </p>
            <Button 
              onClick={() => setIsCreateModalOpen(true)} 
              size="lg"
              className="bg-blue-600 hover:bg-blue-700 shadow-md"
            >
              <Plus className="h-5 w-5 mr-2" />
              Create Your First Class
            </Button>
          </div>
        ) : (
          <>
            {/* Classes Header */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-slate-900">My Classes</h2>
              <p className="text-slate-600 mt-1">
                You have {classes.length} active {classes.length !== 1 ? 'classes' : 'class'}
              </p>
            </div>

            {/* Classes Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {classes.map((classData) => (
                <ClassCard
                  key={classData.id}
                  classData={classData}
                  onClick={() => handleClassClick(classData)}
                />
              ))}
            </div>
          </>
        )}
      </div>

      {/* Create Class Modal */}
      <CreateClassModal
        open={isCreateModalOpen}
        onOpenChange={setIsCreateModalOpen}
        onCreateClass={handleCreateClass}
      />
    </div>
  );
}
