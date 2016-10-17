var mongoose = require('mongoose');

var courseSchema = mongoose.Schema({
	sln:Number,
	prefix:String,
	number:Number,
	nameOfclassName:String,
	days:String,
	start:Number,
	end:Number,
	isSection:Boolean,
	instructor:String,
	isOpen:Boolean,
	generalEd:String,
	isWriting:Boolean,
	link:String
});

courseSchema.statics.createCourse = function (courseModel) {
    return Course.find({ sln: courseModel.sln },
        function (err, course) {
            if (course.length == 0) {
                Course.create({
					sln:courseModel.sln,
					prefix:courseModel.prefix,
					number:courseModel.number,
					nameOfclassName:courseModel.nameOfclassName,
					days:courseModel.days,
					start:courseModel.start,
					end:courseModel.end,
					isSection:courseModel.isSection,
					instructor:courseModel.instructor,
					isOpen:courseModel.isOpen,
					generalEd:courseModel.generalEd,
					isWriting:courseModel.isWriting,
					link:courseModel.link
                }, function (err) {
                    if (err) { return next(err); }
                });
            }
        });
};


courseSchema.statics.getClassByClassName = function (courseModel, cb) {
    return Course.find({ prefix: new RegExp(courseModel.prefix, 'i'), number: courseModel.number}, cb);
};

courseSchema.statics.getClassByDepartment = function (courseModel, cb) {
    return Course.find({ prefix: new RegExp(courseModel.prefix, 'i')}, cb);
};

// Export the User Schema
var Course = mongoose.model('Courses', courseSchema);
module.exports = Course;
