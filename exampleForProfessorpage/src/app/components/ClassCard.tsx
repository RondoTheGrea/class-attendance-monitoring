import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card";
import { Badge } from "@/app/components/ui/badge";
import { BookOpen, Clock, MapPin, Users, Calendar, ArrowRight } from "lucide-react";

interface Schedule {
  day: string;
  startTime: string;
  endTime: string;
}

interface ClassData {
  id: string;
  subject: string;
  section?: string;
  room?: string;
  description?: string;
  schedules: Schedule[];
  announcements: any[];
  attendance: any[];
}

interface ClassCardProps {
  classData: ClassData;
  onClick: () => void;
}

export function ClassCard({ classData, onClick }: ClassCardProps) {
  const getNextSchedule = () => {
    if (classData.schedules.length === 0) {
      return null;
    }

    const now = new Date();
    const currentDay = now.toLocaleDateString('en-US', { weekday: 'long' });
    const currentTime = now.getHours() * 60 + now.getMinutes();

    // Find today's schedules
    const todaySchedules = classData.schedules.filter(s => s.day === currentDay);
    
    for (const schedule of todaySchedules) {
      const [startHour, startMinute] = schedule.startTime.split(':').map(Number);
      const startTimeInMinutes = startHour * 60 + startMinute;
      
      if (startTimeInMinutes > currentTime) {
        return { ...schedule, isToday: true };
      }
    }

    // If no more classes today, find next week's schedule
    const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const currentDayIndex = daysOfWeek.indexOf(currentDay);
    
    for (let i = 1; i <= 7; i++) {
      const nextDayIndex = (currentDayIndex + i) % 7;
      const nextDay = daysOfWeek[nextDayIndex];
      const nextSchedule = classData.schedules.find(s => s.day === nextDay);
      
      if (nextSchedule) {
        return { ...nextSchedule, isToday: false };
      }
    }

    return classData.schedules[0];
  };

  const nextSchedule = getNextSchedule();
  const totalStudents = classData.attendance.reduce((acc, record) => {
    record.students.forEach((student: any) => {
      if (!acc.includes(student.id)) {
        acc.push(student.id);
      }
    });
    return acc;
  }, []).length;

  const formatTime = (time: string) => {
    const [hours, minutes] = time.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
    return `${displayHour}:${minutes} ${ampm}`;
  };

  return (
    <Card 
      className="hover:shadow-xl transition-all duration-300 cursor-pointer border-slate-200 bg-white group hover:-translate-y-1"
      onClick={onClick}
    >
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <CardTitle className="text-xl text-slate-900 mb-2 group-hover:text-blue-600 transition-colors">
              {classData.subject}
            </CardTitle>
            <div className="flex gap-2 flex-wrap">
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
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-2.5 rounded-xl">
            <BookOpen className="h-5 w-5 text-blue-600" />
          </div>
        </div>

        {classData.description && (
          <p className="text-sm text-slate-600 line-clamp-2 leading-relaxed">
            {classData.description}
          </p>
        )}
      </CardHeader>
      
      <CardContent className="space-y-4 pt-0">
        {/* Schedule Information */}
        {nextSchedule ? (
          <div className="bg-slate-50 rounded-lg p-3">
            <div className="flex items-center gap-2 text-sm text-slate-700">
              <Calendar className="h-4 w-4 text-slate-500" />
              <span className="font-medium">{nextSchedule.day}s</span>
              <span className="text-slate-400">•</span>
              <Clock className="h-4 w-4 text-slate-500" />
              <span>{formatTime(nextSchedule.startTime)} - {formatTime(nextSchedule.endTime)}</span>
            </div>
          </div>
        ) : (
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
            <p className="text-sm text-amber-800 font-medium">No schedule configured</p>
          </div>
        )}

        {/* Footer Stats */}
        <div className="flex items-center justify-between pt-3 border-t border-slate-100">
          <div className="flex items-center gap-2">
            <Users className="h-4 w-4 text-slate-400" />
            <span className="text-sm text-slate-600 font-medium">
              {totalStudents} {totalStudents !== 1 ? 'students' : 'student'}
            </span>
          </div>
          <div className="flex items-center gap-1 text-sm font-medium text-blue-600 group-hover:gap-2 transition-all">
            <span>View Details</span>
            <ArrowRight className="h-4 w-4" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
