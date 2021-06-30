ver = release

_EXEC = HQDataServer

BUILD_DIR = bin
SRC_DIRS = ..  #将要编译的cpp文件目录添加到这个变量中，相对目录是build
INC_DIRS= . C:/Boost/include/boost-1_76
LDFLAGS = -LC:/Boost/lib
LDLIBS =-lboost_filesystem -lpthread

CXXFLAGS +=-Wall -fmessage-length=0 -std=c++11 
ifeq ($(ver), debug) #make ver=debug
CXXFLAGS +=-g3
else
CXXFLAGS+=-O3
endif

# Find all the C++ files we want to compile
#SRCS := $(shell find $(SRC_DIRS) -name *.cpp)

# String substitution for every C++ file.
# As an example, $(SRC_DIRS)/hello.cpp turns into $(BUILD_DIR)/hello.o
#OBJS = $(SRCS:$(SRC_DIRS)/%.cpp=$(BUILD_DIR)/%.o)

# String substitution (suffix version without %).
# As an example, .$(BUILD_DIR)/hello.o turns into .$(BUILD_DIR)/hello.d

FIND_FILES=$(shell find $(SRC_DIR) -name *.cpp)
FIND_OBJS=$(FIND_FILES:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)

SRCS:=$(foreach SRC_DIR,$(SRC_DIRS),$(FIND_FILES))
OBJS:=$(foreach SRC_DIR,$(SRC_DIRS),$(FIND_OBJS))

DEPS = $(OBJS:.o=.d)

# Every folder in ./src will need to be passed to GCC so that it can find header files
INC_DIRS += $(shell find $(SRC_DIRS) -type d)
# Add a prefix to INC_DIRS. So moduleA would become -ImoduleA. GCC understands this -I flag
INC_FLAGS = $(addprefix -I,$(INC_DIRS))

# The -MMD and -MP flags together generate Makefiles for us!
# These files will have .d instead of .o as the output.
CPPFLAGS = $(INC_FLAGS) -MMD -MP

# The final build step. 
$(_EXEC): $(OBJS)
	$(CXX) $(LDFLAGS) $(OBJS) -o $@ $(LDLIBS)

# Build step for C++ source
#$(BUILD_DIR)/%.o:$(SRC_DIRS)/%.cpp
#	mkdir -p $(dir $@)
#	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

define BUILD_TEMPLATE 
$(BUILD_DIR)/%.o:$(1)/%.cpp
	mkdir -p $$(dir $$@)
	$$(CXX) $$(CPPFLAGS) $$(CXXFLAGS) -c $$< -o $$@
endef 
$(foreach SRC_DIR,$(SRC_DIRS),$(eval $(call BUILD_TEMPLATE,$(SRC_DIR)))) 

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR) HQDataServer

# Include the .d makefiles. The - at the front suppresses the errors of missing
# Makefiles. Initially, all the .d files will be missing, and we don't want those
# errors to show up.
-include $(DEPS)
