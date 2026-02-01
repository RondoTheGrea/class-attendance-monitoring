import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/app/components/ui/select";
import { Calendar, Clock, Plus, Trash2, AlertCircle } from "lucide-react";
import { Alert, AlertDescription } from "@/app/components/ui/alert";

interface Schedule {
  day: string;
  startTime: string;
  endTime: string;
}

interface ScheduleManagerProps {
  schedules: Schedule[];
  onUpdateSchedules: (schedules: Schedule[]) => void;
}

export function ScheduleManager({ schedules, onUpdateSchedules }: ScheduleManagerProps) {
  const [isAdding, setIsAdding] = useState(false);
  const [newSchedule, setNewSchedule] = useState<Schedule>({
    day: "",
    startTime: "",
    endTime: ""
  });

  const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  const handleAddSchedule = () => {
    if (!newSchedule.day || !newSchedule.startTime || !newSchedule.endTime) {
      alert("Please fill in all fields");
      return;
    }

    // Validate time range
    const [startHour, startMinute] = newSchedule.startTime.split(':').map(Number);
    const [endHour, endMinute] = newSchedule.endTime.split(':').map(Number);
    const startInMinutes = startHour * 60 + startMinute;
    const endInMinutes = endHour * 60 + endMinute;

    if (endInMinutes <= startInMinutes) {
      alert("End time must be after start time");
      return;
    }

    // Check for conflicts
    const hasConflict = schedules.some(schedule => {
      if (schedule.day !== newSchedule.day) return false;

      const [schedStartHour, schedStartMinute] = schedule.startTime.split(':').map(Number);
      const [schedEndHour, schedEndMinute] = schedule.endTime.split(':').map(Number);
      const schedStartInMinutes = schedStartHour * 60 + schedStartMinute;
      const schedEndInMinutes = schedEndHour * 60 + schedEndMinute;

      // Check if times overlap
      return (
        (startInMinutes >= schedStartInMinutes && startInMinutes < schedEndInMinutes) ||
        (endInMinutes > schedStartInMinutes && endInMinutes <= schedEndInMinutes) ||
        (startInMinutes <= schedStartInMinutes && endInMinutes >= schedEndInMinutes)
      );
    });

    if (hasConflict) {
      alert("This schedule conflicts with an existing schedule on the same day");
      return;
    }

    onUpdateSchedules([...schedules, newSchedule]);
    setNewSchedule({ day: "", startTime: "", endTime: "" });
    setIsAdding(false);
  };

  const handleRemoveSchedule = (index: number) => {
    const updatedSchedules = schedules.filter((_, i) => i !== index);
    onUpdateSchedules(updatedSchedules);
  };

  const formatTime = (time: string) => {
    const [hours, minutes] = time.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
    return `${displayHour}:${minutes} ${ampm}`;
  };

  return (
    <div className="space-y-4">
      <Card className="shadow-md border-slate-200">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-slate-900">Weekly Schedule</CardTitle>
            {!isAdding && (
              <Button 
                onClick={() => setIsAdding(true)} 
                size="sm"
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Plus className="h-4 w-4 mr-2" />
                Add Schedule
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {schedules.length === 0 && !isAdding && (
            <div className="text-center py-12">
              <div className="bg-slate-100 rounded-full p-6 w-fit mx-auto mb-4">
                <Calendar className="h-12 w-12 text-slate-400" />
              </div>
              <p className="text-slate-600 font-medium mb-1">No schedules configured</p>
              <p className="text-sm text-slate-500">
                Add class schedules to enable QR code attendance scanning
              </p>
            </div>
          )}

          <div className="space-y-3">
            {schedules.map((schedule, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-slate-50 border border-slate-200 rounded-lg hover:bg-slate-100 transition-colors group"
              >
                <div className="flex items-center gap-4">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <Calendar className="h-5 w-5 text-blue-700" />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">{schedule.day}</p>
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                      <Clock className="h-4 w-4" />
                      <span>
                        {formatTime(schedule.startTime)} - {formatTime(schedule.endTime)}
                      </span>
                    </div>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleRemoveSchedule(index)}
                  className="opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-50 hover:text-red-600"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}

            {isAdding && (
              <Card className="border-2 border-blue-500 shadow-lg">
                <CardContent className="pt-6">
                  <div className="space-y-4">
                    <Alert className="bg-blue-50 border-blue-200">
                      <AlertCircle className="h-4 w-4 text-blue-600" />
                      <AlertDescription className="text-blue-800">
                        Add a new class schedule. Make sure it doesn't conflict with existing schedules.
                      </AlertDescription>
                    </Alert>

                    <div className="grid gap-4">
                      <div>
                        <label className="text-sm font-semibold text-slate-700 mb-2 block">
                          Day of Week
                        </label>
                        <Select
                          value={newSchedule.day}
                          onValueChange={(value) =>
                            setNewSchedule({ ...newSchedule, day: value })
                          }
                        >
                          <SelectTrigger className="border-slate-300">
                            <SelectValue placeholder="Select a day" />
                          </SelectTrigger>
                          <SelectContent>
                            {daysOfWeek.map((day) => (
                              <SelectItem key={day} value={day}>
                                {day}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-semibold text-slate-700 mb-2 block">
                            Start Time
                          </label>
                          <Input
                            type="time"
                            value={newSchedule.startTime}
                            onChange={(e) =>
                              setNewSchedule({ ...newSchedule, startTime: e.target.value })
                            }
                            className="border-slate-300"
                          />
                        </div>

                        <div>
                          <label className="text-sm font-semibold text-slate-700 mb-2 block">
                            End Time
                          </label>
                          <Input
                            type="time"
                            value={newSchedule.endTime}
                            onChange={(e) =>
                              setNewSchedule({ ...newSchedule, endTime: e.target.value })
                            }
                            className="border-slate-300"
                          />
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-2 justify-end pt-2">
                      <Button
                        variant="outline"
                        onClick={() => {
                          setIsAdding(false);
                          setNewSchedule({ day: "", startTime: "", endTime: "" });
                        }}
                      >
                        Cancel
                      </Button>
                      <Button 
                        onClick={handleAddSchedule}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        Add Schedule
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
