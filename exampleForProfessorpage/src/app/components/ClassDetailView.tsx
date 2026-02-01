import { useState } from "react";
import { Button } from "@/app/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs";
import { Badge } from "@/app/components/ui/badge";
import { Input } from "@/app/components/ui/input";
import { Textarea } from "@/app/components/ui/textarea";
import { 
  ArrowLeft, 
  MapPin, 
  Calendar, 
  Bell,
  QrCode,
  Users,
  CheckCircle,
  BookOpen,
  Clock
} from "lucide-react";
import { QRCodeSVG } from "qrcode.react";
import { ScheduleManager } from "@/app/components/ScheduleManager";

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

interface ClassDetailViewProps {
  classData: ClassData;
  onBack: () => void;
  onUpdateClass: (updatedClass: ClassData) => void;
}

export function ClassDetailView({ classData, onBack, onUpdateClass }: ClassDetailViewProps) {
  const [isScanning, setIsScanning] = useState(false);
  const [announcementTitle, setAnnouncementTitle] = useState("");
  const [announcementContent, setAnnouncementContent] = useState("");

  const checkIfClassIsActive = () => {
    const now = new Date();
    const currentDay = now.toLocaleDateString('en-US', { weekday: 'long' });
    const currentTime = now.getHours() * 60 + now.getMinutes();

    return classData.schedules.some(schedule => {
      if (schedule.day !== currentDay) return false;

      const [startHour, startMinute] = schedule.startTime.split(':').map(Number);
      const [endHour, endMinute] = schedule.endTime.split(':').map(Number);
      
      const startTimeInMinutes = startHour * 60 + startMinute;
      const endTimeInMinutes = endHour * 60 + endMinute;

      return currentTime >= startTimeInMinutes && currentTime <= endTimeInMinutes;
    });
  };

  const handleActivateScanning = () => {
    if (classData.schedules.length === 0) {
      alert("Please configure class schedules first before activating QR scanning.");
      return;
    }

    const isActive = checkIfClassIsActive();
    
    if (!isActive) {
      alert("This class is not scheduled for the current time. QR scanning is only available during scheduled class hours.");
      return;
    }

    setIsScanning(true);
  };

  const handlePostAnnouncement = () => {
    if (!announcementTitle.trim() || !announcementContent.trim()) {
      alert("Please fill in both title and content");
      return;
    }

    const newAnnouncement: Announcement = {
      id: Date.now().toString(),
      title: announcementTitle,
      content: announcementContent,
      createdAt: new Date().toISOString()
    };

    const updatedClass = {
      ...classData,
      announcements: [newAnnouncement, ...classData.announcements]
    };

    onUpdateClass(updatedClass);
    setAnnouncementTitle("");
    setAnnouncementContent("");
  };

  const handleUpdateSchedules = (schedules: Schedule[]) => {
    const updatedClass = {
      ...classData,
      schedules
    };
    onUpdateClass(updatedClass);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const qrData = JSON.stringify({
    classId: classData.id,
    className: classData.subject,
    professorId: "PROF001",
    timestamp: new Date().toISOString()
  });

  const uniqueStudents = classData.attendance.reduce((acc, record) => {
    record.students.forEach((student: any) => {
      if (!acc.includes(student.id)) {
        acc.push(student.id);
      }
    });
    return acc;
  }, []).length;

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header Bar */}
      <div className="bg-white border-b shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <Button 
            variant="ghost" 
            onClick={onBack}
            className="mb-4 hover:bg-slate-100"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>

          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4">
              <div className="bg-gradient-to-br from-blue-600 to-blue-700 text-white p-3 rounded-xl shadow-md">
                <BookOpen className="h-6 w-6" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900 mb-2">{classData.subject}</h1>
                <div className="flex gap-2 flex-wrap mb-2">
                  {classData.section && (
                    <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200">
                      Section {classData.section}
                    </Badge>
                  )}
                  {classData.room && (
                    <Badge variant="outline" className="gap-1 border-slate-300">
                      <MapPin className="h-3 w-3" />
                      {classData.room}
                    </Badge>
                  )}
                </div>
                {classData.description && (
                  <p className="text-slate-600 max-w-2xl">{classData.description}</p>
                )}
              </div>
            </div>

            <Button 
              onClick={handleActivateScanning}
              size="lg"
              className="bg-blue-600 hover:bg-blue-700 shadow-md"
            >
              <QrCode className="h-5 w-5 mr-2" />
              Activate QR Scanning
            </Button>
          </div>
        </div>
      </div>

      {/* QR Code Modal */}
      {isScanning && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <Card className="w-full max-w-md shadow-2xl">
            <CardHeader className="text-center pb-4">
              <CardTitle className="text-2xl">Attendance QR Code</CardTitle>
              <p className="text-sm text-slate-600 mt-2">
                Students scan this code to mark attendance
              </p>
            </CardHeader>
            <CardContent className="flex flex-col items-center gap-6">
              <div className="bg-white p-6 rounded-2xl shadow-inner border-4 border-slate-100">
                <QRCodeSVG 
                  value={qrData}
                  size={280}
                  level="H"
                  includeMargin
                />
              </div>
              <div className="text-center bg-slate-50 w-full p-4 rounded-lg">
                <p className="font-medium text-slate-900 mb-1">{classData.subject}</p>
                {classData.section && (
                  <p className="text-sm text-slate-600">Section {classData.section}</p>
                )}
              </div>
              <Button 
                variant="outline" 
                onClick={() => setIsScanning(false)}
                className="w-full"
                size="lg"
              >
                Close Scanner
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Content Tabs */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="grid w-full grid-cols-4 max-w-2xl bg-white shadow-sm h-12">
            <TabsTrigger value="overview" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              Overview
            </TabsTrigger>
            <TabsTrigger value="schedule" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              Schedule
            </TabsTrigger>
            <TabsTrigger value="announcements" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              Announcements
            </TabsTrigger>
            <TabsTrigger value="attendance" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              Attendance
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6 mt-6">
            {/* Class Information Card */}
            <Card className="shadow-md border-slate-200">
              <CardHeader>
                <CardTitle className="text-slate-900">Class Information</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  <div className="space-y-1">
                    <p className="text-sm text-slate-500 font-medium">Subject</p>
                    <p className="font-semibold text-slate-900">{classData.subject}</p>
                  </div>
                  {classData.section && (
                    <div className="space-y-1">
                      <p className="text-sm text-slate-500 font-medium">Section</p>
                      <p className="font-semibold text-slate-900">{classData.section}</p>
                    </div>
                  )}
                  {classData.room && (
                    <div className="space-y-1">
                      <p className="text-sm text-slate-500 font-medium">Room</p>
                      <p className="font-semibold text-slate-900">{classData.room}</p>
                    </div>
                  )}
                  <div className="space-y-1">
                    <p className="text-sm text-slate-500 font-medium">Schedules</p>
                    <p className="font-semibold text-slate-900">{classData.schedules.length} per week</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="shadow-md border-slate-200 bg-gradient-to-br from-blue-50 to-white">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-blue-600 p-3 rounded-xl shadow-sm">
                      <Users className="h-6 w-6 text-white" />
                    </div>
                  </div>
                  <p className="text-3xl font-bold text-slate-900 mb-1">{uniqueStudents}</p>
                  <p className="text-sm text-slate-600 font-medium">Total Students</p>
                </CardContent>
              </Card>

              <Card className="shadow-md border-slate-200 bg-gradient-to-br from-amber-50 to-white">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-amber-600 p-3 rounded-xl shadow-sm">
                      <Bell className="h-6 w-6 text-white" />
                    </div>
                  </div>
                  <p className="text-3xl font-bold text-slate-900 mb-1">{classData.announcements.length}</p>
                  <p className="text-sm text-slate-600 font-medium">Announcements</p>
                </CardContent>
              </Card>

              <Card className="shadow-md border-slate-200 bg-gradient-to-br from-green-50 to-white">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-green-600 p-3 rounded-xl shadow-sm">
                      <Calendar className="h-6 w-6 text-white" />
                    </div>
                  </div>
                  <p className="text-3xl font-bold text-slate-900 mb-1">{classData.attendance.length}</p>
                  <p className="text-sm text-slate-600 font-medium">Sessions Held</p>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="schedule" className="mt-6">
            <ScheduleManager 
              schedules={classData.schedules}
              onUpdateSchedules={handleUpdateSchedules}
            />
          </TabsContent>

          <TabsContent value="announcements" className="space-y-6 mt-6">
            {/* Post New Announcement */}
            <Card className="shadow-md border-slate-200">
              <CardHeader>
                <CardTitle className="text-slate-900">Post New Announcement</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Input
                    placeholder="Announcement title..."
                    value={announcementTitle}
                    onChange={(e) => setAnnouncementTitle(e.target.value)}
                    className="border-slate-300"
                  />
                </div>
                <div>
                  <Textarea
                    placeholder="Write your announcement here..."
                    value={announcementContent}
                    onChange={(e) => setAnnouncementContent(e.target.value)}
                    rows={4}
                    className="border-slate-300"
                  />
                </div>
                <Button 
                  onClick={handlePostAnnouncement} 
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  <Bell className="h-4 w-4 mr-2" />
                  Post Announcement
                </Button>
              </CardContent>
            </Card>

            {/* Announcements List */}
            <div className="space-y-4">
              {classData.announcements.length === 0 ? (
                <Card className="shadow-md border-slate-200">
                  <CardContent className="py-16 text-center">
                    <div className="bg-slate-100 rounded-full p-6 w-fit mx-auto mb-4">
                      <Bell className="h-12 w-12 text-slate-400" />
                    </div>
                    <p className="text-slate-600 font-medium">No announcements yet</p>
                    <p className="text-sm text-slate-500 mt-1">Post your first announcement to keep students informed</p>
                  </CardContent>
                </Card>
              ) : (
                classData.announcements.map((announcement) => (
                  <Card key={announcement.id} className="shadow-md border-slate-200">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <CardTitle className="text-lg text-slate-900">{announcement.title}</CardTitle>
                        <Badge variant="outline" className="border-slate-300 text-slate-600">
                          {formatDate(announcement.createdAt)}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-slate-700 whitespace-pre-wrap leading-relaxed">
                        {announcement.content}
                      </p>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </TabsContent>

          <TabsContent value="attendance" className="space-y-6 mt-6">
            {classData.attendance.length === 0 ? (
              <Card className="shadow-md border-slate-200">
                <CardContent className="py-16 text-center">
                  <div className="bg-slate-100 rounded-full p-6 w-fit mx-auto mb-4">
                    <Users className="h-12 w-12 text-slate-400" />
                  </div>
                  <p className="text-slate-600 font-medium mb-2">No attendance records yet</p>
                  <p className="text-sm text-slate-500 max-w-md mx-auto">
                    Activate QR scanning during scheduled class hours to start recording student attendance
                  </p>
                </CardContent>
              </Card>
            ) : (
              classData.attendance.map((record) => (
                <Card key={record.id} className="shadow-md border-slate-200">
                  <CardHeader>
                    <div className="flex items-center justify-between mb-2">
                      <CardTitle className="text-lg text-slate-900">{formatDate(record.date)}</CardTitle>
                      <Badge className="bg-green-100 text-green-800 border-green-200">
                        {record.students.length} present
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                      <Clock className="h-4 w-4" />
                      <span>{record.scheduleTime}</span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {record.students.map((student) => (
                        <div 
                          key={student.id}
                          className="flex items-center justify-between p-4 bg-slate-50 rounded-lg border border-slate-200"
                        >
                          <div className="flex items-center gap-3">
                            <CheckCircle className="h-5 w-5 text-green-600" />
                            <div>
                              <p className="font-semibold text-slate-900">{student.name}</p>
                              <p className="text-sm text-slate-600">{student.studentId}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-slate-600">
                              {new Date(student.timeScanned).toLocaleTimeString('en-US', {
                                hour: '2-digit',
                                minute: '2-digit'
                              })}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
