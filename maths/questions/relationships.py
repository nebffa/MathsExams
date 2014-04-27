import inspect
import os
import pickle
import random


class DummyPart:
    """A dummy question part for when a question should be structured like so:
        1. (no question text)
            a. some question
            b. some other related question
    """

    def __init__(self):
        self.num_lines, self.num_marks = 0, 0

    def sanity_check(self):
        pass


class QuestionPart:
    """Base class for all question parts.
    """

    is_root = False
    parent = None

    @classmethod
    def storage_paths(cls):
        """Return the paths that are involved in storing this class' questions.
        """
        class_path = inspect.getfile(cls)
        questions_folder, module_name = os.path.split(class_path)

        indices_folder = os.path.join(questions_folder, 'storage', 'indices')
        indices_name = '{module_name}_indices'.format(module_name=module_name)
        indices_path = os.path.join(indices_folder, indices_name)

        data_folder = os.path.join(questions_folder, 'storage', 'data')
        data_name = '{module_name}_{class_name}'.format(module_name=module_name, class_name=cls.__name__)
        data_path = os.path.join(data_folder, data_name)

        return indices_path, data_path

    @classmethod
    def store_question(cls):
        """Store all possible question numbers that have student-friendly values.
        """
        indices_path, data_path = cls.storage_paths()

        byte_indices = [0]
        with open(data_path, 'wb') as f:
            for question in cls.enumerate_questions():
                pickle.dump(question, f)
                byte_indices.append(f.tell())

        if os.path.exists(indices_path):
            with open(indices_path, 'rb') as f:
                cur_indices = pickle.load(f)
        else:
            cur_indices = {}

        cur_indices[cls.__name__] = byte_indices
        with open(indices_path, 'wb') as f:
            pickle.dump(cur_indices, f)

    @classmethod
    def scan_random_question(cls):
        """Return a random set of valid coefficients for this question.
        """
        indices_path, data_path = cls.storage_paths()

        with open(indices_path, 'rb') as f:
            all_indices = pickle.load(f)
            byte_indices = all_indices[cls.__name__]

        with open(data_path, 'rb') as f:
            question_number = random.randint(0, len(byte_indices) - 1)
            first_byte = byte_indices[question_number]
            last_byte = byte_indices[question_number + 1]

            f.seek(first_byte)
            pickled_question = f.read(last_byte - first_byte)

        return pickle.loads(pickled_question)


def root(cls):
    """A class decorator to specify a question root.
    """

    cls.is_root = True
    return cls


def is_child_of(parent):
    """A class decorator to specify a part's parent.
    """

    def decorator(cls):
        cls.parent = parent
        return cls
    return decorator


class PartTree:
    def __init__(self, cls):
        self.cls = cls
        self.children = []  # PartTrees of all the subparts

    def _find_parent(self, cls):
        """A helper function for "add_subpart".

        Given the existing question tree, find out where to insert a new part.
        """
        if cls.parent == self.cls:  # the current node is the parent
            return self
        else:  # check if any of the current node's children is the parent
            for i in self.children:
                if i._find_parent(cls):
                    return i._find_parent(cls)

        raise RuntimeError('The class: {0} could not be located in the tree'.format(cls.__name__))

    def add_subpart(self, cls):
        """Add a new class to the tree.
        """
        child = PartTree(cls)
        parent = self._find_parent(cls)
        parent.children.append(child)

    def _instantiate_tree(self, depth=0, parent=None):
        """Traverse the tree and instantiates an object of each class,
        creating a question for the student to do.
        """

        if depth == 0:  # there's no parent part
            self.object = self.cls()
        elif isinstance(parent, DummyPart):  # there is a dummy for the parent part - there's no information to inherit
            self.object = self.cls()
        else:
            self.object = self.cls(part=parent)

        for child in self.children:
            child._instantiate_tree(depth + 1, self.object)

    def _question_traversal_to_latex(self, depth=0):  # uses the enumitem package which gives us some hbox errors
        """Traverse the tree, returning the latex for each instantiated object.
        """
        total_string = r'\item' + '\n'

        if depth == 0:
            total_string += '\n'

        if not hasattr(self.object, 'question_statement'):
            total_string += '$ $'
        else:
            total_string += self.object.question_statement() + '\n'

        if self.object.num_lines != 0:
            total_string += r'\fillwithlines{{{0}in}}'.format(self.object.num_lines / 4) + '\n'

        if self.children:
            total_string += r'\begin{parts}' + '\n' + '\n'.join(
                i._question_traversal_to_latex(depth + 1) for i in self.children) + r'\end{parts}' + '\n'

        return total_string + '\n'

    def _solution_traversal_to_latex(self, depth=0):  # uses the enumitem package which gives us some hbox errors
        """Traverse the tree, returning the latex for each instantiated object.
        """
        total_string = r'\item' + '\n'

        if depth == 0:
            total_string += '\n'

        if not hasattr(self.object, 'solution_statement'):
            total_string += '$ $'
        else:
            total_string += self.object.solution_statement() + '\n'

        if self.children:
            total_string += r'\begin{parts}' + '\n' + '\n'.join(
                i._solution_traversal_to_latex(depth + 1) for i in self.children) + r'\end{parts}' + '\n'

        return total_string + '\n'

    def write_question(self, f):
        self._instantiate_tree()
        f.write(self._question_traversal_to_latex())

    def write_solution(self, f):
        f.write(self._solution_traversal_to_latex())

    def show_question(self):
        """Return a question's latex (assuming the question tree has already been populated).
        """
        self._instantiate_tree()
        return self._question_traversal_to_latex()


def parse_structure(module):
    """Parse the question structure based on the relationships of classes in a module.

    Will be evolved over time!!!
    """
    classes = []

    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, QuestionPart):  # get all the question parts
            classes.append(obj)

    roots = [i for i in classes if i.is_root]
    no_dummy_parent = all([i.parent != DummyPart for i in classes])
    if len(roots) != 1 and no_dummy_parent:
        raise RuntimeError('There needs to be 1 and only 1 root in {0}'.format(module.__name__))

    if not no_dummy_parent:
        root_part = DummyPart
        classes.append(DummyPart)
    else:
        root_part = roots[0]

    def invalid_part(cls):
        """Returns false for any class that neither is the question root nor has a parent.
        """
        if not cls.is_root and cls.parent is None:
            return True
        else:
            return False

    root_node = PartTree(root_part)
    classes.remove(root_part)
    while classes:
        for i in range(len(classes)):
            cls = classes[i]
            if invalid_part(cls):
                raise ValueError('The part: {0} is neither the root part nor a subpart.'.format(cls.__name__))

            root_node.add_subpart(cls)
            classes.remove(cls)
            break  # we just removed something from the list, so we need to reset our iterator variable

    return root_node
